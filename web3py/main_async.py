import asyncio

import argparse
import os
from datetime import datetime

import numpy as np
import pandas as pd

from contract_functions import ContractTest
from settings import DEBUG, RESULTS_CSV_DIR


def between_callback(process_count: int, fn: str):
    global df
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    func_to_run = fn + '()'
    try:
        df_to_append = loop.run_until_complete(get_time(func_to_run, process_count))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()

    df = pd.concat([df, df_to_append], ignore_index=True)


async def get_time(func_to_run: str, process_count: int) -> pd.DataFrame:
    # Flag statuses
    cloud_status_ok = False
    function_status_ok = False
    # Values to store
    cloud_address = 'NaN'
    start_cloud, end_cloud = datetime.now(), datetime.now()
    start_fun, end_fun = datetime.now(), datetime.now()

    try:
        if 'cloud_sla_creation_activation' in func_to_run:
            start_cloud, start_fun = datetime.now(), datetime.now()
            cloud_address, cloud_status_ok = await eval(func_to_run)
            end_cloud, end_fun = datetime.now(), datetime.now()
            function_status_ok = cloud_status_ok
        else:
            start_cloud = datetime.now()
            cloud_address, cloud_status_ok = await obj.cloud_sla_creation_activation()
            end_cloud = datetime.now()
            func_to_run = func_to_run.replace(')', f"'{cloud_address}')")
            start_fun = datetime.now()
            function_status_ok = await eval(func_to_run)
            end_fun = datetime.now()
    except ValueError as v:
        if DEBUG:
            print(f'ValueError #{process_count}: {v}')
        cloud_status_ok = False
        function_status_ok = False
        end_cloud = datetime.now()
        end_fun = datetime.now()
    finally:
        duration_cloud = end_cloud - start_cloud
        duration_fun = end_fun - start_fun

        return pd.DataFrame({
            'id': [process_count],
            'start_cloud': [(start_cloud - zero_time).total_seconds()],
            'end_cloud': [(end_cloud - zero_time).total_seconds()],
            'time_cloud': [duration_cloud.total_seconds()],
            'start_fun': [(start_fun - zero_time).total_seconds()],
            'end_fun': [(end_fun - zero_time).total_seconds()],
            'time_fun': [duration_fun.total_seconds()],
            'address': [cloud_address],
            'status': cloud_status_ok and function_status_ok,
        })


async def main():
    global df

    for idx in range(args.threads):
        df_to_append = await get_time('obj.' + args.function + '()', idx)
        df = pd.concat([df, df_to_append], ignore_index=True)
        rand = np.random.exponential(1 / args.lambda_p)
        await asyncio.sleep(rand)

    '''
    print(df[['id', 'start_cloud', 'end_cloud', 'time_cloud', 'start_fun', 'end_fun', 'time_fun']])
    print(f"Status column:\n{df['status']}")
    print(f"Rows with status True: {len(df.loc[df['status']])}")
    '''

    if args.save:
        path = os.getcwd()
        out_dir = os.path.join(path, RESULTS_CSV_DIR)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        out_file = f'async_{args.function}_{args.lambda_p}_{args.threads}_{args.blockchain}.csv'
        results_path = os.path.join(out_dir, out_file)
        df.to_csv(results_path, index=False, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Script written using web3py to test different blockchains.',
        usage='%(prog)s blockchain function [-t TIME] [-l LAMBDA] [-s]'
    )
    parser.add_argument(
        'blockchain', default='none', type=str,
        choices=['polygon', 'besu', 'go-quorum'],
        help='the name of the blockchain'
    )
    parser.add_argument(
        'function', default='none', type=str,
        choices=[
            'cloud_sla_creation_activation',
            'upload',
            'read',
            'delete',
            'file_check_undeleted_file',
            'another_file_upload',
            'read_deny_lost_file_check',
            'another_file_upload_read',
            'corrupted_file_check'
        ],
        help='the name of the function to stress'
    )
    parser.add_argument(
        '-t', '--threads', default=10,
        type=int,
        help='the number of async threads to run'
    )
    parser.add_argument(
        '-l', '--lambda_p', default=.5,
        type=float, choices=[2, 1, .5, .2, .1],
        help='the lambda parameter for interarrival time Poisson'
    )
    parser.add_argument(
        '-s', '--save', default=False,
        action='store_true',
        help='save csv file as output'
    )

    args = parser.parse_args()

    df = pd.DataFrame()
    obj = ContractTest(args.blockchain)
    zero_time = datetime.now()

    exit(asyncio.run(main()))

import asyncio

import argparse
import os
import threading
from datetime import datetime

import numpy as np
import pandas as pd

from web3client import Web3Client
from contract_functions import ContractTest
from settings import DEBUG, RESULTS_CSV_DIR, DEPLOYED_CONTRACTS
from utility import range_limited_thread, init_simulation


def between_callback(process_count: int, fn: str):
    global df
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    func_to_run = fn + '()'
    df_to_append = loop.run_until_complete(get_time(func_to_run, process_count))
    loop.close()
    df = pd.concat([df, df_to_append], ignore_index=True)


async def get_time(func_to_run: str, process_count: int) -> pd.DataFrame:
    # Flag statuses
    function_status_ok = False
    # Values to store
    cloud_address = 'NaN'
    start_fun, end_fun = datetime.now(), datetime.now()

    try:
        if 'cloud_sla_creation_activation' == func_to_run:
            start_fun = datetime.now()
            cloud_address, function_status_ok = await eval(func_to_run)
            end_fun = datetime.now()
        else:
            start_fun = datetime.now()
            function_status_ok = await eval(func_to_run)
            end_fun = datetime.now()
    except ValueError as v:
        if DEBUG:
            print(f'ValueError #{process_count}: {v}')
        function_status_ok = False
        end_fun = datetime.now()
    finally:
        duration_fun = end_fun - start_fun

        return pd.DataFrame({
            'id': [process_count],
            'start_fun': [(start_fun - zero_time).total_seconds()],
            'end_fun': [(end_fun - zero_time).total_seconds()],
            'time_fun': [duration_fun.total_seconds()],
            'address': [cloud_address],
            'status': function_status_ok,
        })


async def main():
    init = await init_simulation(contracts, args.threads, args.function)
    if not init:
        print('MSG INIT NON RIUSCITA')
        exit(1)

    print('MSG INIT RIUSCITA')
    jobs = []

    for idx in range(args.threads):
        circular = idx % DEPLOYED_CONTRACTS
        thread = threading.Thread(target=between_callback, args=[idx, f'contracts[{circular}].{args.function}'])
        jobs.append(thread)

    # Start the threads
    for j in jobs:
        j.start()
        rand = np.random.exponential(1 / args.lambda_p)
        await asyncio.sleep(rand)

    # Ensure all the threads have finished
    for j in jobs:
        j.join()

    if DEBUG:
        print(df)
        print(f"Status column:\n{df[['id', 'status']]}")
        print(f"Rows with status True: {len(df.loc[df['status']])}")

    if args.save:
        path = os.getcwd()
        out_dir = os.path.join(path, RESULTS_CSV_DIR)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        out_file = f'async_thread_{args.function}_{args.lambda_p}_{args.threads}_{args.blockchain}.csv'
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
        type=range_limited_thread,
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

    zero_time = datetime.now()
    df = pd.DataFrame()
    client = Web3Client(args.blockchain)
    summary = client.get_contract_address()

    '''
    for idx, elm in enumerate(summary):
        print(f'[{idx}]:\n {json.dumps(elm, indent=4, sort_keys=True)}')
    '''

    contracts = []
    for i in range(DEPLOYED_CONTRACTS):
        circle = i % DEPLOYED_CONTRACTS  # TODO: not manually
        contracts.append(
            ContractTest(
                client.get_w3(),
                client.get_w3_async(),
                client.pks_to_addresses(summary[circle]['private_keys']),
                summary[circle]['private_keys'],
                summary[circle]['contracts']
            )
        )

    print('Start simulation...')
    exit(asyncio.run(main()))

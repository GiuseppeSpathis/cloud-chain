import asyncio

import argparse
import threading
from datetime import datetime

import pandas as pd

from contract_functions import ContractTest


def between_callback(process_count: int, fn: str):
    global df
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    func_to_run = fn + '()'
    df_to_append = loop.run_until_complete(get_time(func_to_run, process_count))
    loop.close()
    df = pd.concat([df, df_to_append], ignore_index=True)


async def get_time(func_to_run: str, process_count: int):
    if 'cloud_sla_creation_activation' not in func_to_run:
        cloud_address, _ = await obj.cloud_sla_creation_activation()
        # TODO check middle statuses?
        func_to_run = func_to_run.replace(')', f"'{cloud_address}')")

    start = datetime.now()

    if 'cloud_sla_creation_activation' in func_to_run:
        address, all_status_ok = await eval(func_to_run)
    else:
        all_status_ok = await eval(func_to_run)
        address = 'NaN'

    end = datetime.now()

    duration = end - start

    return pd.DataFrame({
        'id': [process_count],
        'start': [(start - zero_time).total_seconds()],
        'end': [(end - zero_time).total_seconds()],
        'duration': [duration.total_seconds()],
        'address': [address],
        'status': all_status_ok,
    })


async def main():
    threads = 100  # Number of threads to create
    jobs = []

    for idx in range(threads):
        thread = threading.Thread(target=between_callback, args=[idx, 'obj.cloud_sla_creation_activation'])
        jobs.append(thread)

    # Start the threads
    for j in jobs:
        j.start()
        await asyncio.sleep(0.6)

    # Ensure all the threads have finished
    for j in jobs:
        j.join()

    print(df[['id', 'start', 'end', 'duration', 'status']])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Create description.',
        usage='%(prog)s'
    )
    parser.add_argument(
        'settings', default='none', type=str,
        choices=['polygon', 'consensys-quorum'],
        help='the name of the blockchain'
    )

    args = parser.parse_args()

    zero_time = datetime.now()
    df = pd.DataFrame()
    obj = ContractTest(args.settings)

    exit(asyncio.run(main()))

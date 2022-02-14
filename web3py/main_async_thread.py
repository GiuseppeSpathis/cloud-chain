import asyncio
import json

import argparse
import threading
from datetime import datetime

from eth_typing import Address
from web3 import Web3, AsyncHTTPProvider, HTTPProvider
from web3.contract import Contract
from web3.eth import AsyncEth
from web3.middleware import geth_poa_middleware

import pandas as pd

from settings import (
    COMPILED_FACTORY_PATH,
    COMPILED_ORACLE_PATH,
    COMPILED_CLOUD_SLA_PATH,
    DEBUG, HTTP_URI
)


def between_callback(process_count: int, fn: str):
    global df
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    func_to_run = fn + f'({process_count})'
    df_to_append = loop.run_until_complete(get_time(func_to_run, process_count))
    loop.close()
    df = pd.concat([df, df_to_append], ignore_index=True)


async def get_time(func_to_call: str, process_count: int):
    start = datetime.now()

    address = await eval(func_to_call)

    end = datetime.now()

    duration = end - start

    return pd.DataFrame({
        'id': [process_count],
        'start': [(start - zero_time).total_seconds()],
        'end': [(end - zero_time).total_seconds()],
        'duration': [duration.total_seconds()],
        'address': [address]
    })


def update_nonces():
    global nonces

    for i in range(3):
        nonces[i] = w3.eth.get_transaction_count(accounts[i])


def get_addresses(blockchain: str) -> tuple:
    if blockchain == 'polygon':
        from settings import (
            POLYGON_FACTORY_ADDRESS, POLYGON_ORACLE_ADDRESS
        )
        return POLYGON_FACTORY_ADDRESS, POLYGON_ORACLE_ADDRESS
    from settings import (
        QUORUM_FACTORY_ADDRESS, QUORUM_ORACLE_ADDRESS
    )
    return QUORUM_FACTORY_ADDRESS, QUORUM_ORACLE_ADDRESS


def get_settings(blockchain: str) -> tuple:
    if blockchain == 'polygon':
        from settings import (
            polygon_accounts, polygon_private_keys
        )
        return polygon_accounts, polygon_private_keys
    from settings import (
        quorum_accounts, quorum_private_keys
    )
    return quorum_accounts, quorum_private_keys


def get_contract(address: Address, compiled_contract_path: str) -> Contract:
    def get_abi(path: str) -> list:
        with open(path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json['abi']
        return contract_abi

    abi = get_abi(compiled_contract_path)
    contract = w3.eth.contract(address=address, abi=abi)

    return contract


async def sign_send_transaction(tx: dict, pk: str):
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=pk)
    tx_hash = await w3_async.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = await w3_async.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt


async def cloud_sla_creation_activation(process_count: int) -> str:
    global nonces

    # start = datetime.now()
    # Parameters
    price = Web3.toWei(5, 'ether')
    test_validity_duration = 60 ** 2

    # Contracts
    contract_factory = get_contract(FACTORY_ADDRESS, COMPILED_FACTORY_PATH)
    contract_oracle = get_contract(ORACLE_ADDRESS, COMPILED_ORACLE_PATH)

    # Transactions
    tx_create_child = contract_factory.functions.createChild(
        contract_oracle.address,
        accounts[1],
        price,
        test_validity_duration,
        1,
        1
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[0],
        'nonce': nonces[0] + process_count
    })
    await sign_send_transaction(tx_create_child, private_keys[0])

    tx_sm_address = contract_factory.functions.getSmartContractAddress(
        accounts[1]
    ).call()

    # Contract
    contract_cloud_sla = get_contract(tx_sm_address, COMPILED_CLOUD_SLA_PATH)

    # Transaction
    tx_deposit = contract_cloud_sla.functions.Deposit().buildTransaction({
        'gasPrice': 0,
        'from': accounts[1],
        'nonce': nonces[1] + process_count,
        'value': price
    })
    await sign_send_transaction(tx_deposit, private_keys[1])

    if DEBUG:
        print('CloudSLA creation and activation: OK')
        print(f'\taddress: {tx_sm_address}')
    # end = datetime.now()

    # duration = end - start

    '''
    return pd.DataFrame({
        'id': [process_count],
        'start': [(start - zero_time).total_seconds()],
        'end': [(end - zero_time).total_seconds()],
        'duration': [duration.total_seconds()],
        'address': [tx_sm_address]
    })'''
    return tx_sm_address


'''
async def sequence_upload(filepath: str, hash_digest: str):
    # Contract
    contract_cloud_sla = get_contract(cloud_sla_address, COMPILED_CLOUD_SLA_PATH)

    # Transactions
    challenge = Web3.solidityKeccak(
        ['bytes32'], [hash_digest]
    )

    tx_upload_request = contract_cloud_sla.functions.UploadRequest(
        filepath,
        challenge
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[1],
        'nonce': w3.eth.get_transaction_count(accounts[1])
    })
    await sign_send_transaction(tx_upload_request, private_keys[1])

    tx_upload_request_ack = contract_cloud_sla.functions.UploadRequestAck(
        filepath
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[0],
        'nonce': w3.eth.get_transaction_count(accounts[0])
    })
    await sign_send_transaction(tx_upload_request_ack, private_keys[0])

    tx_upload_transfer_ack = contract_cloud_sla.functions.UploadTransferAck(
        filepath,
        hash_digest
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[0],
        'nonce': w3.eth.get_transaction_count(accounts[0])
    })
    await sign_send_transaction(tx_upload_transfer_ack, private_keys[0])


async def upload(process_count: int) -> pd.DataFrame:
    # Parameters
    filepath = 'test.pdf'
    hash_digest = '0x9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'

    start = datetime.now()
    await sequence_upload(filepath, hash_digest)
    end = datetime.now()

    if DEBUG:
        print('Upload: OK')

    duration = end - start

    return pd.DataFrame({
        'id': [process_count],
        'start': [(start - zero_time).total_seconds()],
        'end': [(end - zero_time).total_seconds()],
        'duration': [duration.total_seconds()]
    })
'''


async def main():
    global cloud_sla_address

    cloud_sla_address = await cloud_sla_creation_activation(0)
    update_nonces()

    threads = 10  # Number of threads to create
    jobs = []
    for i in range(threads):
        thread = threading.Thread(target=between_callback, args=[i, 'cloud_sla_creation_activation'])
        jobs.append(thread)

    # Start the threads
    for j in jobs:
        j.start()
        await asyncio.sleep(0.25)

    # Ensure all the threads have finished
    for j in jobs:
        j.join()

    print(df[['id', 'start', 'end', 'duration']])


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
    FACTORY_ADDRESS, ORACLE_ADDRESS = get_addresses(args.settings)
    cloud_sla_address = Address(b'0x0')

    accounts, private_keys = get_settings(args.settings)

    zero_time = datetime.now()
    df = pd.DataFrame()

    w3_async = Web3(
        AsyncHTTPProvider(HTTP_URI),
        modules={
            'eth': AsyncEth
        },
        middlewares=[]  # geth_poa_middleware not supported yet
    )

    w3 = Web3(HTTPProvider(HTTP_URI))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(f'-- Connection established --')

    nonces = []
    for idx in range(3):
        nonces.append(w3.eth.get_transaction_count(accounts[idx]))

    exit(asyncio.run(main()))

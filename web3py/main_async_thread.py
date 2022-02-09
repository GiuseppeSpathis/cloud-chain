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

from settings import (
    COMPILED_FACTORY_PATH,
    COMPILED_ORACLE_PATH,
    COMPILED_CLOUD_SLA_PATH,
    DEBUG, HTTP_URI
)


def between_callback(process_count):
    # TODO manage args for all functions
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(cloud_sla_creation_activation(process_count))
    loop.close()


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


async def cloud_sla_creation_activation(process_count):
    start = datetime.now()
    print(f'Start process#{process_count} at time {start.strftime("%H:%M:%S.%f")}')
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
        'nonce': await w3_async.eth.get_transaction_count(accounts[0])
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
        'nonce': await w3_async.eth.get_transaction_count(accounts[1]),
        'value': price
    })
    await sign_send_transaction(tx_deposit, private_keys[1])

    if DEBUG:
        print('CloudSLA creation and activation: OK')
        print(f'\taddress: {tx_sm_address}')
    end = datetime.now()
    print(f'End process#{process_count} at time {end.strftime("%H:%M:%S.%f")}', end='\n\n')
    return tx_sm_address


async def main():
    global cloud_sla_address

    threads = 10  # Number of threads to create
    jobs = []
    for i in range(0, threads):
        thread = threading.Thread(target=between_callback, args=[i])
        jobs.append(thread)

    # Start the threads
    for j in jobs:
        j.start()
        await asyncio.sleep(.2)

    # Ensure all the threads have finished
    for j in jobs:
        j.join()


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

    exit(asyncio.run(main()))

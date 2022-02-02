import json
import os
from time import time

import argparse
from web3 import Web3
from web3.auto import w3
from web3.middleware import geth_poa_middleware

from settings import (
    COMPILED_FACTORY_PATH,
    COMPILED_ORACLE_PATH,
    COMPILED_CLOUD_SLA_PATH,
    DEBUG, WEB_SOCKET_URI
)


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


def get_contract_abi(compiled_contract_path: str) -> list:
    if DEBUG:
        print(f'-- Get contract abi for {os.path.basename(compiled_contract_path)} --')
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']
    return contract_abi


def sign_transaction(tx: dict, pk: str, label: str):
    if DEBUG:
        print('-- Start sign transaction --')
        print(f'{label}: {json.dumps(tx, indent=4, sort_keys=True)}')

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=pk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if DEBUG:
        tx_receipt_json = json.loads(Web3.toJSON(tx_receipt))
        print(f'{label}_receipt: {json.dumps(tx_receipt_json, indent=4, sort_keys=True)}')
        print('-- End sign transaction --')


def cloud_sla_creation_activation():
    factory_abi = get_contract_abi(COMPILED_FACTORY_PATH)
    oracle_abi = get_contract_abi(COMPILED_ORACLE_PATH)

    contract_factory = w3.eth.contract(address=FACTORY_ADDRESS, abi=factory_abi)
    contract_oracle = w3.eth.contract(address=ORACLE_ADDRESS, abi=oracle_abi)

    w3.eth.default_account = accounts[0]
    price = Web3.toWei(5, 'ether')
    test_validity_duration = 60 ** 2
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
        'nonce': w3.eth.get_transaction_count(accounts[0])
    })
    sign_transaction(tx_create_child, private_keys[0], label='create_child')

    w3.eth.defaultAccount = accounts[1]
    tx_sm_address = contract_factory.functions.getSmartContractAddress(
        accounts[1]
    ).call()

    cloud_sla_abi = get_contract_abi(COMPILED_CLOUD_SLA_PATH)
    contract_cloud_sla = w3.eth.contract(address=tx_sm_address, abi=cloud_sla_abi)

    tx_deposit = contract_cloud_sla.functions.Deposit().buildTransaction({
        'gasPrice': 0,
        'from': accounts[1],
        'nonce': w3.eth.get_transaction_count(accounts[1]),
        'value': price
    })
    sign_transaction(tx_deposit, private_keys[1], label='deposit')


def main():
    durations = []
    for _ in range(10):
        start = time()
        cloud_sla_creation_activation()
        end = time()
        durations.append(end - start)

    print(durations)
    print(f'avg_durations: {round(sum(durations) / len(durations), 2)}')


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
    accounts, private_keys = get_settings(args.settings)

    if not w3.isConnected():
        print(f'-- Connection error --')
        w3 = Web3(Web3.WebsocketProvider(WEB_SOCKET_URI))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(f'-- Connection established --')

    exit(main())

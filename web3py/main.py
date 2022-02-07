import json

import argparse

from eth_typing import Address
from web3 import Web3
from web3.auto import w3
from web3.contract import Contract
from web3.middleware import geth_poa_middleware

from settings import (
    COMPILED_FACTORY_PATH,
    COMPILED_ORACLE_PATH,
    COMPILED_CLOUD_SLA_PATH,
    WEB_SOCKET_URI
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


def get_contract(address: Address, compiled_contract_path: str) -> Contract:
    def get_abi(path: str) -> list:
        with open(path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json['abi']
        return contract_abi

    abi = get_abi(compiled_contract_path)
    contract = w3.eth.contract(address=address, abi=abi)

    return contract


def sign_send_transaction(tx: dict, pk: str):
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=pk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    return tx_receipt


def cloud_sla_creation_activation():
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
        'nonce': w3.eth.get_transaction_count(accounts[0])
    })
    sign_send_transaction(tx_create_child, private_keys[0])

    tx_sm_address = contract_factory.functions.getSmartContractAddress(
        accounts[1]
    ).call()

    # Contract
    contract_cloud_sla = get_contract(tx_sm_address, COMPILED_CLOUD_SLA_PATH)

    # Transaction
    tx_deposit = contract_cloud_sla.functions.Deposit().buildTransaction({
        'gasPrice': 0,
        'from': accounts[1],
        'nonce': w3.eth.get_transaction_count(accounts[1]),
        'value': price
    })
    sign_send_transaction(tx_deposit, private_keys[1])

    print('CloudSLA creation and activation: OK')
    print(f'\taddress: {tx_sm_address}')
    return tx_sm_address


def sequence_upload(filepath: str, hash_digest: str):
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
    sign_send_transaction(tx_upload_request, private_keys[1])

    tx_upload_request_ack = contract_cloud_sla.functions.UploadRequestAck(
        filepath
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[0],
        'nonce': w3.eth.get_transaction_count(accounts[0])
    })
    sign_send_transaction(tx_upload_request_ack, private_keys[0])

    tx_upload_transfer_ack = contract_cloud_sla.functions.UploadTransferAck(
        filepath,
        hash_digest
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[0],
        'nonce': w3.eth.get_transaction_count(accounts[0])
    })
    sign_send_transaction(tx_upload_transfer_ack, private_keys[0])


def sequence_read(filepath: str, url: str):
    # Contract
    contract_cloud_sla = get_contract(cloud_sla_address, COMPILED_CLOUD_SLA_PATH)

    # Transactions
    tx_read_request = contract_cloud_sla.functions.ReadRequest(
        filepath
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[1],
        'nonce': w3.eth.get_transaction_count(accounts[1])
    })
    sign_send_transaction(tx_read_request, private_keys[1])

    tx_read_request_ack = contract_cloud_sla.functions.ReadRequestAck(
        filepath,
        url
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[0],
        'nonce': w3.eth.get_transaction_count(accounts[0])
    })
    sign_send_transaction(tx_read_request_ack, private_keys[0])


def sequence_file(filepath: str, url: str, hash_digest: str):
    # Contracts
    contract_cloud_sla = get_contract(cloud_sla_address, COMPILED_CLOUD_SLA_PATH)
    contract_oracle = get_contract(ORACLE_ADDRESS, COMPILED_ORACLE_PATH)

    # Transactions
    tx_file_hash_request = contract_cloud_sla.functions.FileHashRequest(
        filepath
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[1],
        'nonce': w3.eth.get_transaction_count(accounts[1])
    })
    sign_send_transaction(tx_file_hash_request, private_keys[1])

    tx_digit_store = contract_oracle.functions.DigestStore(
        url,
        hash_digest
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[2],
        'nonce': w3.eth.get_transaction_count(accounts[2])
    })
    sign_send_transaction(tx_digit_store, private_keys[2])

    tx_file_check = contract_cloud_sla.functions.FileCheck(
        filepath
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[1],
        'nonce': w3.eth.get_transaction_count(accounts[1])
    })
    sign_send_transaction(tx_file_check, private_keys[1])


def upload():
    # Parameters
    filepath = 'test.pdf'
    hash_digest = '0x9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'

    sequence_upload(filepath, hash_digest)

    print('Upload: OK')


def read():
    # Parameters
    filepath = 'test.pdf'
    url = 'www.test.com'

    sequence_read(filepath, url)

    print('Read: OK')


def delete():
    # Parameter
    filepath = 'test.pdf'

    # Contract
    contract_cloud_sla = get_contract(cloud_sla_address, COMPILED_CLOUD_SLA_PATH)

    # Transactions
    tx_delete_request = contract_cloud_sla.functions.DeleteRequest(
        filepath
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[1],
        'nonce': w3.eth.get_transaction_count(accounts[1])
    })
    sign_send_transaction(tx_delete_request, private_keys[1])

    tx_delete = contract_cloud_sla.functions.Delete(
        filepath
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[0],
        'nonce': w3.eth.get_transaction_count(accounts[0])
    })
    sign_send_transaction(tx_delete, private_keys[0])

    print('Delete: OK')


def file_check_undeleted_file():
    # Parameters
    filepath = 'test.pdf'
    url = 'www.test.com'
    hash_digest = '0x9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'

    sequence_file(filepath, url, hash_digest)

    print('File check for undeleted file: OK')


def another_file_upload():
    # Parameters
    filepath = 'test2.pdf'
    hash_digest = '0x1f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'

    sequence_upload(filepath, hash_digest)

    print('Another file upload: OK')


def read_deny_lost_file_check():
    # Parameter
    filepath = 'test2.pdf'

    # Contract
    contract_cloud_sla = get_contract(cloud_sla_address, COMPILED_CLOUD_SLA_PATH)

    # Transactions
    tx_read_request = contract_cloud_sla.functions.ReadRequest(
        filepath
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[1],
        'nonce': w3.eth.get_transaction_count(accounts[1])
    })
    sign_send_transaction(tx_read_request, private_keys[1])

    tx_read_request_deny = contract_cloud_sla.functions.ReadRequestDeny(
        filepath
    ).buildTransaction({
        'gasPrice': 0,
        'from': accounts[0],
        'nonce': w3.eth.get_transaction_count(accounts[0])
    })
    sign_send_transaction(tx_read_request_deny, private_keys[0])

    print('Read Deny with lost file check: OK')


def another_file_upload_read():
    # Parameters
    filepath = 'test3.pdf'
    url = 'www.test3.com'
    hash_digest = '0x2f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'

    sequence_upload(filepath, hash_digest)
    sequence_read(filepath, url)

    print('Another file upload + read: OK')


def corrupted_file_check():
    # Parameters
    filepath = 'test3.pdf'
    url = 'www.test3.com'
    hash_digest = '0x4f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'

    sequence_file(filepath, url, hash_digest)

    print('File Check for corrupted file: OK')


def main():
    global cloud_sla_address

    cloud_sla_address = cloud_sla_creation_activation()
    upload()
    read()
    delete()
    file_check_undeleted_file()
    another_file_upload()
    read_deny_lost_file_check()
    another_file_upload_read()
    corrupted_file_check()


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

    if not w3.isConnected():
        print(f'-- Connection error --')
        # TODO connection based on blockchain
        w3 = Web3(Web3.WebsocketProvider(WEB_SOCKET_URI))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    print(f'-- Connection established --')

    exit(main())

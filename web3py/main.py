import os
import json

from web3 import Web3
from web3.auto import w3
from web3.middleware import geth_poa_middleware

from settings import (
    WEB_SOCKET_URI,
    COMPILED_FACTORY_PATH, DEPLOYED_FACTORY_ADDRESS,
    COMPILED_ORACLE_PATH, DEPLOYED_ORACLE_ADDRESS,COMPILED_CLOUDSLA_PATH,
    accounts, private_keys
)


def get_contract_abi(compiled_contract_path: str) -> list:
    print(f'Get contract abi for {os.path.basename(compiled_contract_path)}')
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)
        contract_abi = contract_json['abi']
    return contract_abi


def sign_transaction(tx: dict, pk: str, label: str, log: bool = False):
    if log:
        print('-' * 50)
        print(f'{label}: {json.dumps(tx, indent=4, sort_keys=True)}', end='\n\n')

    signed_tx = w3.eth.account.sign_transaction(tx, private_key=pk)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    if log:
        tx_receipt_json = json.loads(Web3.toJSON(tx_receipt))
        print(f'{label}_receipt: {json.dumps(tx_receipt_json, indent=4, sort_keys=True)}')
        print('-' * 50)


if not w3.isConnected():
    # w3 = Web3(Web3.HTTPProvider(HTTP_URI))
    w3 = Web3(Web3.WebsocketProvider(WEB_SOCKET_URI))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

factory_abi = get_contract_abi(COMPILED_FACTORY_PATH)
oracle_abi = get_contract_abi(COMPILED_ORACLE_PATH)

# CloudSLA creation and activation
contract_factory = w3.eth.contract(address=DEPLOYED_FACTORY_ADDRESS, abi=factory_abi)
print(f"All Factory functions: {contract_factory.all_functions()}")

contract_oracle = w3.eth.contract(address=DEPLOYED_ORACLE_ADDRESS, abi=oracle_abi)
print(f"All FileDigestOracle functions: {contract_oracle.all_functions()}")

w3.eth.default_account = accounts[0]
price = Web3.toWei(5, 'ether')
test_validity_duration = 60 ** 2
tx_create_child = contract_factory.functions.createChild(
    DEPLOYED_ORACLE_ADDRESS,
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
sign_transaction(tx_create_child, private_keys[0], label='create_child', log=True)

w3.eth.defaultAccount = accounts[1]
tx_sm_address = contract_factory.functions.getSmartContractAddress(
    accounts[1]
).call()
print(f'get_sm_address: {tx_sm_address}')

cloudsla_abi = get_contract_abi(COMPILED_CLOUDSLA_PATH)
myinstance = w3.eth.contract(address=tx_sm_address, abi=cloudsla_abi)

tx_deposit=myinstance.functions.Deposit().buildTRansaction({
    'gasPrice': 0,
    'from': accounts[1],
    'nonce': w3.eth.get_transaction_count(accounts[0]),
    'value': price
})
sign_transaction(tx_deposit, private_keys[1], label='Deposit', log=True)

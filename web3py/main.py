import web3
import json
from web3 import Web3
from web3.middleware import geth_poa_middleware

'''
# HTTPProvider:
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))

# Convenience method to automatically detect the provider
from web3.auto import w3
print(f'Auto detect: {w3.isConnected()}')
'''

blockchain_address = 'ws://127.0.0.1:8546'

# Local providers
w3 = Web3(Web3.WebsocketProvider(blockchain_address))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.defaultAccount = w3.eth.accounts[0]

compiled_factory_path = '../build/contracts/Factory.json'
deployed_factory_address = '0x6486A01e45648B1aDCc51D375Af3a7c0a5e9002a'

compiled_oracle_path = '../build/contracts/FileDigestOracle.json'
deployed_oracle_address = '0x7cb50610e7e107b09acf3FBB8724C6df3f3e1c1d'

with open(compiled_factory_path) as file:
    contract_factory_json = json.load(file)
    contract_factory_abi = contract_factory_json['abi']

with open(compiled_oracle_path) as file:
    contract_oracle_json = json.load(file)
    contract_oracle_abi = contract_oracle_json['abi']

contract_factory = w3.eth.contract(address=deployed_factory_address, abi=contract_factory_abi)
print(f"All Factory functions: {contract_factory.all_functions()}")

contract_oracle = w3.eth.contract(address=deployed_oracle_address, abi=contract_oracle_abi)
print(f"All FileDigestOracle functions: {contract_oracle.all_functions()}")

price = Web3.toWei(5, 'ether')
test_validity_duration = 60 ** 2
# print(contract_factory.functions.createChild(deployed_oracle_address, ))

'''
print(f"Block number: {w3.eth.block_number}")
last_block = json.loads(Web3.toJSON(w3.eth.get_block('latest')))
print(f'Last block: {json.dumps(last_block, indent=4, sort_keys=True)}')

balance = w3.eth.get_balance('0x627306090abaB3A6e1400e9345bC60c78a8BEf57')
print(f'Balance (wei): {balance}')
print(f"Balance (eth): {Web3.fromWei(balance, 'ether')}")
'''

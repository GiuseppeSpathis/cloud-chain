from web3.auto import w3
from solcx import install_solc, compile_files

from settings import polygon_accounts

install_solc(version='latest')

compiled_sol = compile_files(
    '../contracts/FileDigestOracle.sol',
    output_values=['abi', 'bin']
)

contract_id, contract_interface = compiled_sol.popitem()

bytecode = contract_interface['bin']
abi = contract_interface['abi']

w3.eth.default_account = polygon_accounts[0]

Factory = w3.eth.contract(abi=abi, bytecode=bytecode)
tx_hash = Factory.constructor().transact()
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f'Contract address: {tx_receipt.contractAddress}')

factory = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)
print(f'All Factory functions: {factory.all_functions()}')
print(f'Factory address: {factory.address}')

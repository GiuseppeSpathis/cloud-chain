from web3.auto import w3
from solcx import install_solc, compile_files

from settings import polygon_accounts, polygon_private_keys

install_solc(version='latest')


def deploy_contract(filename: str, address: int = 0):
    compiled_sol = compile_files(
        f'../contracts/{filename}',
        output_values=['abi', 'bin']
    )

    contract_id, contract_interface = compiled_sol.popitem()

    bytecode = contract_interface['bin']
    abi = contract_interface['abi']

    w3.eth.default_account = polygon_accounts[address]

    Contract = w3.eth.contract(abi=abi, bytecode=bytecode)

    tx = Contract.constructor().buildTransaction({
        'gasPrice': 0,
        'from': w3.eth.default_account,
        'nonce': w3.eth.get_transaction_count(w3.eth.default_account)
    })
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=polygon_private_keys[address])
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    contract = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=abi
    )
    print(f"All {filename} functions: {contract.all_functions()}")
    print(f'\tAddress: {contract.address}')


deploy_contract('Migrations.sol')
deploy_contract('FileDigestOracle.sol', address=2)
deploy_contract('Factory.sol')
deploy_contract('CloudSLA.sol')

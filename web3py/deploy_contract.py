import json
import os

from web3.auto import w3
from solcx import compile_files, set_solc_version, install_solc

from settings import polygon_accounts, polygon_private_keys


def deploy_contract(filename: str, address: int = 0):
    old_cwd = os.getcwd()
    filename_no_ext = filename.split('.')[0]
    key = f'{filename}:{filename_no_ext}'

    install_solc('0.8.9')
    set_solc_version('0.8.9')

    os.chdir('../contracts')
    compiled_sol = compile_files(
        filename,
        output_values=['abi', 'bin']
    )

    os.chdir('../build/contracts')
    with open(f"{filename_no_ext}.json", 'w') as file:
        json.dump(compiled_sol[key], file, indent=4)  # [key]

    if 'Factory' in filename:
        with open("CloudSLA.json", 'w') as file:
            json.dump(compiled_sol["CloudSLA.sol:CloudSLA"], file, indent=4)

    os.chdir(old_cwd)

    bytecode = compiled_sol[key]['bin']
    abi = compiled_sol[key]['abi']

    '''
    bytecode = compiled_sol['contracts'][filename][filename_no_ext]['evm']['bytecode']['object']
    abi = json.loads(
        compiled_sol['contracts'][filename][filename_no_ext]['metadata']
    )['output']['abi']
    '''

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
    print(f'All {filename} functions: {contract.all_functions()}')
    print(f'\tAddress: {contract.address}')


deploy_contract('Migrations.sol')
deploy_contract('FileDigestOracle.sol', address=2)
deploy_contract('Factory.sol')

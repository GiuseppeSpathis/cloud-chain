import json
import os

from eth_typing import ChecksumAddress, Address
from semantic_version import Version
from solcx import install_solc, set_solc_version, compile_files, get_installed_solc_versions
from web3 import Web3, AsyncHTTPProvider, HTTPProvider
from web3.eth import AsyncEth

from settings import HTTP_URI, SOLC_VERSION, CONFIG_DIR, DEPLOYED_CONTRACTS
from utility import get_credentials


class Web3Client:
    def __init__(self, blockchain: str):
        self.w3_async = Web3(
            AsyncHTTPProvider(HTTP_URI),
            modules={
                'eth': AsyncEth
            },
            middlewares=[]  # geth_poa_middleware not supported yet
        )
        self.w3 = Web3(HTTPProvider(HTTP_URI))
        self.blockchain = blockchain
        self.status_init = False

    def init_contracts(self) -> []:
        summary = []
        private_keys = get_credentials(self.blockchain)
        contract_names = ['Migrations.sol', 'FileDigestOracle.sol', 'Factory.sol', 'Aggregator.sol']
        #contract_names = ['Migrations.sol', 'FileDigestOracle.sol', 'Factory.sol']

        print('Start deploy...')
        i = 0
        it = iter(private_keys)
        
        for pk_factory, pkSLA, pk_oracle_1, pk_oracle_2, pk_oracle_3, pk_oracle_4, pk_oracle_5, pk_aggregator in zip(it, it, it, it, it, it, it, it):  
            
            if i >= DEPLOYED_CONTRACTS:
                break
            
            oracle_addresses = []
            # Deploy 5 FileDigestOracle contracts
            #j = 0
            for pk_oracle in [pk_oracle_1, pk_oracle_2, pk_oracle_3, pk_oracle_4, pk_oracle_5]: 
                #j += 1
                oracle_addresses.append(self.__deploy_contract(contract_names[1], pk_oracle))

            # Deploy Factory contract
            factory_address = self.__deploy_contract(contract_names[2], pk_factory) 
            
            # Deploy Aggregator contract, passing the list of oracle addresses
            aggregator_address = self.__deploy_contract(contract_names[3], pk_aggregator, oracle_addresses) 

            summary.append({
                'contracts': {
                    contract_names[1]: oracle_addresses, # Store list of oracle addresses
                    contract_names[2]: factory_address,
                    contract_names[3]: aggregator_address
                },
                'private_keys': [pk_factory, pkSLA, pk_oracle_1, pk_oracle_2, pk_oracle_3, pk_oracle_4, pk_oracle_5, pk_aggregator],
                'cloud_address': '0x0',
                'tx_upload_count': 0
            })
            i += 1
        '''
        for pk_0, pk_1, pk_2 in zip(it, it, it): #pk2 e' FileDigestOracle e pk1 e' sla e pk0 e' factory
            if i >= DEPLOYED_CONTRACTS:
                break
            contract_addresses = []
            for contract in contract_names:
                pk = pk_2 if contract == contract_names[1] else pk_0

                if contract != contract_names[0]:
                    contract_addresses.append(self.__deploy_contract(contract, pk))

            summary.append({
                'contracts': {
                    contract_names[1]: contract_addresses[0],
                    contract_names[2]: contract_addresses[1]
                },
                'private_keys': [pk_0, pk_1, pk_2],
                'cloud_address': '0x0',
                'tx_upload_count': 0
            })
            i += 1
        '''
        filename = f'{self.blockchain}.json'
        filepath = os.path.join(os.getcwd(), CONFIG_DIR, filename)
        with open(filepath, 'w') as file:
            json.dump(summary, file, indent=4)
        print('Deploy completed.')
        print(f'Config file saved to {filepath}')
        self.status_init = True
        return summary
        
    def pks_to_addresses(self, pks: []) -> []:
        addresses = []
        for pk in pks:
            addresses.append(
                self.w3.eth.account.privateKeyToAccount(pk).address
            )
            
        return addresses if len(addresses) > 1 else addresses[0]

    def __deploy_contract(self, filename: str, pk: Address, oracle_addresses: list = None) -> ChecksumAddress:
        old_cwd = os.getcwd()
        filename_no_ext = filename.split('.')[0]
        key = f'{filename}:{filename_no_ext}'

        if Version(SOLC_VERSION) not in get_installed_solc_versions():
            install_solc(SOLC_VERSION)
        set_solc_version(SOLC_VERSION)

        os.chdir('../contracts')
        compiled_sol = compile_files(
            filename,
            output_values=['abi', 'bin']
        )

        os.chdir('../build/contracts')
        with open(f'{filename_no_ext}.json', 'w') as file:
            json.dump(compiled_sol[key], file, indent=4)

        # TODO: review
        if 'Factory' in filename:
            with open('CloudSLA.json', 'w') as file:
                json.dump(compiled_sol['CloudSLA.sol:CloudSLA'], file, indent=4)

        os.chdir(old_cwd)

        bytecode = compiled_sol[key]['bin']
        abi = compiled_sol[key]['abi']

        self.w3.eth.default_account = self.pks_to_addresses([pk])

        Contract = self.w3.eth.contract(abi=abi, bytecode=bytecode)

        if 'Aggregator' in filename:
            tx = Contract.constructor(oracle_addresses).buildTransaction({
                'gasPrice': 0,
                'from': self.w3.eth.default_account,
                'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account)
            })
        else:
            tx = Contract.constructor().buildTransaction({
                'gasPrice': 0,
                'from': self.w3.eth.default_account,
                'nonce': self.w3.eth.get_transaction_count(self.w3.eth.default_account)
            })
            
        signed_tx = self.w3.eth.account.sign_transaction(tx, private_key=pk)
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        contract = self.w3.eth.contract(
            address=tx_receipt.contractAddress,
            abi=abi
        )
        return contract.address

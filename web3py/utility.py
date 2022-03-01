import json
import os
from argparse import ArgumentTypeError

from eth_typing import Address
from web3.contract import Contract

from settings import MIN_THREAD, MAX_THREAD, DEPLOYED_CONTRACTS, CONFIG_DIR


async def init_simulation(contracts: [], threads, fn: str) -> bool:
    statuses = []
    try:
        for c in contracts:
            # Use different cloud_addresses for each contract instance
            cloud_address, cloud_status_ok = await c.cloud_sla_creation_activation()
            c.set_cloud_sla_address(cloud_address)
            statuses.append(cloud_status_ok)
            if fn == 'read' or fn == 'read_deny_lost_file_check' or fn == 'file_check_undeleted_file':
                statuses.append(await c.upload())
            if fn == 'file_check_undeleted_file':
                statuses.append(await c.read())
            if fn == 'corrupted_file_check':
                statuses.append(await c.another_file_upload_read())
            if fn == 'delete':
                for _ in range(round(threads / DEPLOYED_CONTRACTS) + 1):
                    statuses.append(await c.upload())
    except ValueError as v:
        # TODO: think about
        print(f'ValueError [init_sim]: {v}')
    else:
        return check_statuses(statuses)


def get_credentials(blockchain: str) -> tuple:
    if blockchain == 'polygon':
        from settings import (
            polygon_accounts, polygon_private_keys
        )
        return polygon_accounts, polygon_private_keys
    from settings import (
        quorum_accounts, quorum_private_keys
    )
    return quorum_accounts, quorum_private_keys


def get_contract(w3, address: Address, compiled_contract_path: str) -> Contract:
    def get_abi(path: str) -> list:
        with open(path) as file:
            contract_json = json.load(file)
            contract_abi = contract_json['abi']
        return contract_abi

    abi = get_abi(compiled_contract_path)
    contract = w3.eth.contract(address=address, abi=abi)

    return contract


def check_statuses(statuses: []) -> bool:
    for idx in range(len(statuses)):
        if statuses[idx] == 0:
            return False
    return True


def get_contracts_config(blockchain: str):
    print('Retrieve config file...')
    filename = f'{blockchain}.json'
    filepath = os.path.join(os.getcwd(), CONFIG_DIR, filename)
    with open(filepath) as file:
        contracts_summary = json.loads(file.read())
    print(f'Config file retrieved at {filepath}.')
    return contracts_summary


def range_limited_thread(arg: str) -> int:
    """
    Type function for argparse - int within some predefined bounds.
    """
    try:
        s = int(arg)
    except ValueError:
        raise ArgumentTypeError("must be a int number")
    if s < MIN_THREAD or s > MAX_THREAD:
        raise ArgumentTypeError(f"argument must be < {str(MIN_THREAD)} and > {str(MAX_THREAD)}")
    return s

import json
from argparse import ArgumentTypeError

from eth_typing import Address
from web3.contract import Contract

from settings import MIN_THREAD, MAX_THREAD


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

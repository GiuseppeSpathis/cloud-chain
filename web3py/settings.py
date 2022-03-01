import json
from string import Template

HTTP_URI = 'http://127.0.0.1:8545'

SOLC_VERSION = '0.8.9'

__COMPILED_CONTRACT_PATH = Template('../build/contracts/${contract}')
COMPILED_FACTORY_PATH = __COMPILED_CONTRACT_PATH.substitute(contract='Factory.json')
COMPILED_ORACLE_PATH = __COMPILED_CONTRACT_PATH.substitute(contract='FileDigestOracle.json')
COMPILED_CLOUD_SLA_PATH = __COMPILED_CONTRACT_PATH.substitute(contract='CloudSLA.json')

CONFIG_DIR = 'config'
RESULTS_CSV_DIR = 'results'

DEPLOYED_CONTRACTS = 8

# Preloaded accounts
__BESU_QUORUM_PATH = Template('../besu_quorum_scripts/src/${filename}')
with open(__BESU_QUORUM_PATH.substitute(filename='private_keys.json')) as file:
    quorum_private_keys = json.loads(file.read())['privatekey']

__POLYGON_PATH = Template('../polygon/src/${filename}')
with open(__POLYGON_PATH.substitute(filename='address.json')) as file:
    polygon_accounts = json.loads(file.read())['address']

with open(__POLYGON_PATH.substitute(filename='private_keys.json')) as file:
    polygon_private_keys = json.loads(file.read())['privatekey']

DEBUG = True
MIN_THREAD = 1
MAX_THREAD = 10000

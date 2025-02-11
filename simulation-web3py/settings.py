import json
from string import Template

HTTP_URI = 'http://127.0.0.1:8545'

SOLC_VERSION = '0.8.9'

__COMPILED_CONTRACT_PATH = Template('../build/contracts/${contract}')
COMPILED_FACTORY_PATH = __COMPILED_CONTRACT_PATH.substitute(contract='Factory.json')
COMPILED_ORACLE_PATH = __COMPILED_CONTRACT_PATH.substitute(contract='FileDigestOracle.json')
COMPILED_AGGREGATOR_PATH = __COMPILED_CONTRACT_PATH.substitute(contract='Aggregator.json')
COMPILED_CLOUD_SLA_PATH = __COMPILED_CONTRACT_PATH.substitute(contract='CloudSLA.json')

CONFIG_DIR = 'config'
RESULTS_CSV_DIR = 'results'

NUM_TRANSACTIONS = 1 # quante volte la singola funzione viene lanciata
#quanti contratti sla vengono creati, questo numero poi fa dipendere 
#pure il numero di chiavi per contratto e il numero di account della blockchain presente in run_polygon
DEPLOYED_CONTRACTS = 1#40 

#__QUORUM_PATH = '../quorum/src/private_keys.json'
#with open(__QUORUM_PATH) as file:
#    quorum_private_keys = json.loads(file.read())['privatekey']

__POLYGON_PATH = Template('../polygon/src/${filename}')
with open(__POLYGON_PATH.substitute(filename='private_keys.json')) as file:
    polygon_private_keys = json.loads(file.read())['privatekey']

DEBUG = True
MIN_VAL = 0
MAX_VAL = 10000

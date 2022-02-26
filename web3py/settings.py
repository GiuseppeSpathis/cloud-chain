import json

HTTP_URI = 'http://127.0.0.1:8545'
WEB_SOCKET_URI = 'ws://127.0.0.1:8546'

COMPILED_FACTORY_PATH = '../build/contracts/Factory.json'
COMPILED_ORACLE_PATH = '../build/contracts/FileDigestOracle.json'
COMPILED_CLOUD_SLA_PATH = '../build/contracts/CloudSLA.json'

DEPLOYED_CONTRACTS = 5

RESULTS_CSV_DIR = 'results'

# Preloaded accounts
quorum_accounts = [
    '0xFE3B557E8Fb62b89F4916B721be55cEb828dBd73',
    '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
    '0xf17f52151EbEF6C7334FAD080c5704D77216b732',
    '0x376e04384e6ea7f9391168B4FC440c8D23a475dc'
]
quorum_private_keys = [
    '0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63',
    '0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3',
    '0xae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f',
    '0xa65fac6daf7a9c04da01ae753df5cb6057914f25241cbda1407aee609ffd1996'
]

with open('../polygon/src/address.json') as file:
    polygon_accounts = json.loads(file.read())['address']

with open('../polygon/src/private_keys.json') as file:
    polygon_private_keys = json.loads(file.read())['privatekey']

DEBUG = True
MIN_THREAD = 1
MAX_THREAD = 10000

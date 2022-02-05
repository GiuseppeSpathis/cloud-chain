import json

HTTP_URI = 'http://127.0.0.1:8545'
WEB_SOCKET_URI = 'ws://127.0.0.1:8546'

COMPILED_FACTORY_PATH = '../build/contracts/Factory.json'
COMPILED_ORACLE_PATH = '../build/contracts/FileDigestOracle.json'
COMPILED_CLOUD_SLA_PATH = '../build/contracts/CloudSLA.json'

QUORUM_FACTORY_ADDRESS = '0xa1dc9167B1a8F201d15b48BdD5D77f8360845ceD'
QUORUM_ORACLE_ADDRESS = '0x3536Ca51D15f6fc0a76c1f42693F7949b5165F0D'

POLYGON_FACTORY_ADDRESS = '0x0D9f89fC392585AbB5139eE80be4c8a3bC78997f'
POLYGON_ORACLE_ADDRESS = '0xA91E39C55b7E61baB92fA72915Da64711c979292'

# Preloaded accounts
quorum_accounts = [
    '0xFE3B557E8Fb62b89F4916B721be55cEb828dBd73',
    '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
    '0xf17f52151EbEF6C7334FAD080c5704D77216b732'
]
quorum_private_keys = [
    '0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63',
    '0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3',
    '0xae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f'
]

with open('../polygon/src/address.json') as file:
    polygon_accounts = json.loads(file.read())['address']

with open('../polygon/src/private_keys.json') as file:
    polygon_private_keys = json.loads(file.read())['privatekey']

DEBUG = True

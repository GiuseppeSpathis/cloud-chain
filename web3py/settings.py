import json
from string import Template

HTTP_URI = 'http://127.0.0.1:8545'

SOLC_VERSION = '0.8.9'

__COMPILED_CONTRACT_PATH = Template('../build/contracts/${contract}')
COMPILED_FACTORY_PATH = __COMPILED_CONTRACT_PATH.substitute(contract='Factory.json')
COMPILED_ORACLE_PATH = __COMPILED_CONTRACT_PATH.substitute(contract='FileDigestOracle.json')
COMPILED_CLOUD_SLA_PATH = __COMPILED_CONTRACT_PATH.substitute(contract='CloudSLA.json')

CONFIG_PATH = Template('./config/${blockchain}.json')

DEPLOYED_CONTRACTS = 1

RESULTS_CSV_DIR = 'results'

# Preloaded accounts
quorum_accounts = [
    '0xFE3B557E8Fb62b89F4916B721be55cEb828dBd73',
    '0x627306090abaB3A6e1400e9345bC60c78a8BEf57',
    '0xf17f52151EbEF6C7334FAD080c5704D77216b732',
    '0x376e04384e6ea7f9391168B4FC440c8D23a475dc',
    '0x60efEc3534d94a109d74218d3f56672a9A1De751',
    '0x2A3FBFFbcdB320141f512Ef8d8B7c8F148f2ffBF',
    '0xe46B2dA15E59d7bD87512fE8B71C1Bb34440C193',
    '0xc242390713f973b233c670fd6a58b190ca764355',
    '0x3472F01524f319C42524e40563d2067c256dD3A0',
    '0xad3eC07E0211e228ae7a8D8053AFb2C217F70b5B',
    '0x4889eAEa7C40F5f3Ac18Cc965C83086D23CCe4Ed',
    '0x4e5821fA9786DE5A36c57F1E945db026C016d369',
    '0x8D0251a95cF0e0E0E13dE1D735FEc0352544E507',
    '0x09Fa6732F6f12E983c9ED88C5fC3EB85dBBae84F',
    '0xe655E6fAce11E6F31273ec305EAC9f156d04D760',
    '0xf01c21821612e4EA7c2B569CcfA1677B8Ed85bDf',
    '0xA2BFD3DB8A7fD7309CF828F9da60922Fb46C968D',
    '0xcc048aE72672314bA8ed6625aB063012c3391470'
]
quorum_private_keys_old = [
    '0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63',
    '0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3',
    '0xae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f',
    '0xa65fac6daf7a9c04da01ae753df5cb6057914f25241cbda1407aee609ffd1996',
    '0x21e3e9806742b02077a35057d682451ccc612c22d134286c968f1cad2fcca202',
    '0x4f5d9c424bb497d17a318308221af181294e104f21b6e7b8e5cf5acbfd7c6ece',
    '0x8536e0b113049b7f224264f5536987f28a4fadbefbf8b689ef8afc11b4f48202',
    '0xb99ecd5729322ab9cd0c0c2e03f1331e61532242574ca7fbf758775d9d56f845',
    '0x4e7ee5922252e9953941c7ea96ebbc9ab4d55a131f48b0031910e8395e46f0ae',
    '0x69747c8007e17c35d357be4155492f2d1ca7481bb9e1471da6630a288a41cf85',
    '0x4311a4cd2b70895bb1bd3d5bc1a6024807acb33875275bf7104a0e78964b8a6f',
    '0xcb09cc90388b61b7fbefbaf9a22194ba85dcb1c921bb82dfed235bb9e23f5e09',
    '0xe0962ad56a30fcdd9e497c4ad2da50341a29f7ab7f67e48a5f6ade1d111949b4',
    '0x1961ba0da02af23a8fd08eee2351010dc31c95c06a1906d182ef71099af985ef',
    '0xf555802793acc3ea5dad62b6b53d7c272b80444ac27d0bacde840f3c70c6687a',
    '0xd405847ac6cde646c830c8a656dc4afc58bdbc07a859728e8c8c513e8dc91678',
    '0x54004c337e99f8800f6b71626afc64d7b24884c84a6c4f33a1890774ac76dc6f',
    '0xf1abc74a176c2ece35c81dc7531fee59ce4bc755ebc391c3fcffa624af0da316'
]

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

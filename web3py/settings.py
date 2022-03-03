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
quorum_private_keys = [
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
    '0xf1abc74a176c2ece35c81dc7531fee59ce4bc755ebc391c3fcffa624af0da316',
    '0x2c48a9b39cf841667259e0666d9f308e099b884a14a456d8875a426c8e56506f',
    '0xdb260e2bdfeb9e8de1f4093a66f7db04725347d1704c40a53b2f196a4dd80e63',
    '0x28fb7a4108d76bddfaa1f484a6099ce17e9e9f4613c30adfb04bc6baff354ecc',
    '0x5e8401e48f01a5244c3c29f32cf5b71a5cde8f4f825f870d55a0fccba9a2694f',
    '0x2b625d84178524b6318f1314c6c78d421f74b22d1b396dc492caa3bde4673703',
    '0x90f7c030bb597cfb1fc2d08c4455df8a61159b376c3c9b2eff646e2309609e64',
    '0x22eaae77c41e9bb272a66ebefc27beb36bca13ada949d0123f9d22b1cd6d6d92'
]

__POLYGON_PATH = Template('../polygon/src/${filename}')
with open(__POLYGON_PATH.substitute(filename='private_keys.json')) as file:
    polygon_private_keys = json.loads(file.read())['privatekey']

DEBUG = True
MIN_VAL = 0
MAX_VAL = 10000

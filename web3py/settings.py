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

DEPLOYED_CONTRACTS = 10

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
    '0x22eaae77c41e9bb272a66ebefc27beb36bca13ada949d0123f9d22b1cd6d6d92',
    '0xc7c5365c1c6f0e6b51208ee7220c65893e6bcb5f1fa7b4dffc774816e8f30ddf',
    '0xe0e3092cf9be62d8fc3eb04b839f74fefbe97b360bb34e6415a1c89413222ba3',
    '0xfbdd0d37c2ef3d8836d002d7884531fd66d5d11276604abbf0819860c5ad5e0f',
    '0xc18b244c64b1ab9dd1ea099e6869746d4a6a4df5f5f4e8ec68c684767d562f06',
    '0x263be8a1f2820301f51fb57c3b21a57bef2b98f4f07500d45f82d66f372b2508',
    '0x3f02cd6466c815baa8631f51a6429ef1fe4445cc9b52565fe447c5bc74dd58a2',
    '0x48c9d99a24ae045b1d7c706568b12383eaf08ef458348436f2147a77a520b6e2',
    '0xd04d5946f0f42643e3b5db0882e775f63122973908315ee77f85fd9856be6852',
    '0x1db231f5473be22def3c5633b4a06ff93fef189b2270b98e20f8c8d73b00b1ab',
    '0x8c0bd4cdf5d592f18f146a8cc3da36adbcc1d6c9de38962e9aecf82c2f7884c7',
    '0x9d51cff271c2ca61eb41671a1c7f21cb6a606869ad3ddb9def6ee29e97c3eaeb',
    '0x5a779dfcd0fdda47d22d521df69f5feda0ed6158a8f266491526ec368e31e3ae',
    '0x84b73c8f0b9675cfe9de316b24eee214d95eb612c25d8f7ac43f1207acd5da40',
    '0x6ddfd3a240a730d0dd3fbe0078a74950c83bcd07cdacf41e25e75c8a40b51dd0',
    '0x66819ddea586b3a0be3c794a604b3976490a3b9f7b785c24b6d5ad01354539bf',
    '0x689f999b613523c2e01510480436b25c9d998ce8bcb3399aaeb0d7102fb912c4',
    '0x72bca73da66f3b163a92e3871af02f7288371b464653d0b54d84f8ed2c7a7cd8',
    '0xd1d1da76564818991b5bd02c98b36d3279539832cfa11da95ca29fd8437854f1',
    '0x6d6ac8f144971e1e93e2ba20c5271c83de9f8bf2ce2d4c58aa62f87d14097ca3',
    '0xc61557f0b64870bc8fe76adb1dafaf08fc95f3ecd6ee1c7265e3bdb00748b111',
    '0xb14d6ce4511f9d4c3b4bd5d552ee3c3d17a01871e1d93205739c74cb16bf5a76',
    '0x45bddfc33197819eca5ff538b86a94125fba7554bcf2d20e094fcc5ee7d02540',
    '0x17787d4afea916ea22e3f5ef3e3060af0e800690f1f637da4250b372ee09511f',
    '0xde30a8048b269a23e4126a48fa544c40f49c03f31b7643ffef885b770559ca92',
    '0x82b0be9c5cf8dfb7cde6432116e06967096c67c97c1bcadcacca6beeb0b791d1',
    '0x7ca30e8322bd5236cf12cf60b8946e66da308a0686ed6cb9e610f000aab1d63f',
    '0xb44aa7a043f001fad429f8afb78f6a5cac1a7ef5bafd93b911d9f75f8bcc913c',
    '0x1db8d6846d6f2b9f03464261584119b4be37ba37619309aa35496f532fc878fc',
    '0x31d835f2782203d848569d9b21692e41311681adaf8baf1fafb75f81aa3f1718',
    '0x91af0376741c38726d8247ce2443c1b57c7ab142f2b36be9206b2e649a568452',
    '0xaee4dc9283a35946b2663e595dcb8a665bf47a9fd44b6954abfb7cd18c79f296',
    '0xb2bf34624b24e95c3cef4eb8ac73749f80510269884f89cdae4cbcb4b5403b88',
    '0x1f1b135a13975c0874af26c47b2c62a905305c0ac34b3e509a74efbd6adde159',
    '0x8133742ce8c26a570386cbae1eaf6ebd667f18712afd6b8d39dfdd9e7eaad387',
    '0x2ac72de98a2065a4382d7fba8e670ebe85d4f3c2ada3d48786e8b6c502115c97'
]

__POLYGON_PATH = Template('../polygon/src/${filename}')
with open(__POLYGON_PATH.substitute(filename='private_keys.json')) as file:
    polygon_private_keys = json.loads(file.read())['privatekey']

DEBUG = True
MIN_VAL = 0
MAX_VAL = 10000

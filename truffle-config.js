const dotenv = require('dotenv');
const HDWalletProvider = require('truffle-hdwallet-provider');
const Web3 = require('web3');
const wsProvider = new Web3.providers.WebsocketProvider('ws://localhost:8546');
const httpProvider = new Web3.providers.HttpProvider('http://localhost:8545');

// insert the private key of the accounts
// address of account 0 (12 in metamask) : 0xFE3B557E8Fb62b89F4916B721be55cEb828dBd73
dotenv.config();
const privateKeys = [
    '0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63',
    '0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3',
    '0xae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f',
];
const polygonPrivateKeys = [
    '0xfa8c34684f6321f6694670b80d84b2aea4c050e3af9de52eaff7161a2547f18d',
    '0xa203f405515611f7779be34f1a3319e9dfb245b07824a7e9573ca1dbcb2c129e',
    '0x45e0cc52b902c8400490c51a4d3711bc53ae5d2d655a5bb4df5f1f3861c9de6c',
];

module.exports = {
    // See <http://truffleframework.com/docs/advanced/configuration>
    // for more about customizing your Truffle configuration!
    networks: {
        development: {
            host: '127.0.0.1',
            port: 8545,
            network_id: '*', // Match any network id
            gasPrice: 0,
        },
        quickstartWallet: {
            provider: () => {
                HDWalletProvider.prototype.on = wsProvider.on.bind(wsProvider);
                return new HDWalletProvider(privateKeys, wsProvider, 0, 3);
            },
            network_id: '*',
            gasPrice: 0,
            type: 'quorum',
            websockets: true,
        },
        polygon: {
            provider: () =>
                new HDWalletProvider(polygonPrivateKeys, httpProvider, 0, 3),
            network_id: '*',
            type: 'quorum',
            gasPrice: 0,
        },
    },
    compilers: {
        solc: {
            version: '0.8.9', // Fetch exact version from solc-bin (default: truffle's version)
            // docker: true,        // Use "0.5.1" you've installed locally with docker (default: false)
            // settings: {          // See the solidity docs for advice about optimization and evmVersion
            //  optimizer: {
            //    enabled: false,
            //    runs: 200
            //  },
            evmVersion: 'byzantium',
            // }
        },
    },
};
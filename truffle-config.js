const dotenv = require('dotenv');
const HDWalletProvider = require('truffle-hdwallet-provider');
const Web3 = require('web3');
const wsProvider = new Web3.providers.WebsocketProvider('ws://localhost:8546');
const httpProvider = new Web3.providers.HttpProvider('http://localhost:8545');
var pkPolygon = require('./polygon/src/private_keys.json');

// insert the private key of the accounts
// address of account 0 (12 in metamask) : 0xFE3B557E8Fb62b89F4916B721be55cEb828dBd73
dotenv.config();
const privateKeys = [
    '0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63',
    '0xc87509a1c067bbde78beb793e6fa76530b6382a4c0241e5e4a9ec0a0f44dc0d3',
    '0xae6ae8e5ccbfb04590405997ee2d52d2b330726137b875053c36d94e974d162f',
];
//const polygonPrivateKeys = [ '0x70c796883d614c0b77b53c8d4371772ea1edd2e2527706e4879c6e84179273df' , '0xb283ac8163deff09ba0700e64d3496ab83f9c8a0a85f254fe907cdb7beab379a' , '0xe583b446b20cfba9947c56b0998808824eac509a6c26718eae59da7a2d99c520' , '0xe2c2ffde111be1ba4de14b969af9a1dde837a9d3d5034ac940047bbbf3cdb7bc' ];
const polygonPrivateKeys = pkPolygon.privatekey
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
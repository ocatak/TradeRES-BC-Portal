const HDWalletProvider = require('@truffle/hdwallet-provider');
const fs = require('fs');
const path = require('path');

// First, read in the mnemonic from a file to keep it secret
const mnemonicPath = path.resolve(__dirname, '.secret');
const mnemonic = fs.existsSync(mnemonicPath) ? fs.readFileSync(mnemonicPath, {encoding: 'utf8'}).trim() : '';

module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",
      port: 7545, // This is the default port for Ganache
      network_id: "*", // Match any network id
    },
    rinkeby: {
      provider: function() {
        return new HDWalletProvider(mnemonic, `https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID`);
      },
      network_id: 4, // Rinkeby's id
      gas: 5500000, // Rinkeby has a lower block limit than mainnet
      confirmations: 2, // # of confs to wait between deployments. (default: 0)
      timeoutBlocks: 200, // # of blocks before a deployment times out  (minimum/default: 50)
      skipDryRun: true, // Skip dry run before migrations? (default: false for public nets )
    },
    // Configuration for main Ethereum network (requires more funds and caution)
    mainnet: {
      provider: function() {
        return new HDWalletProvider(mnemonic, `https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID`);
      },
      network_id: 1,
      gas: 5500000,
      gasPrice: 10000000000, // 10 Gwei
    }
  },

  // Set default mocha options here, use special reporters, etc.
  mocha: {
    // timeout: 100000
  },

  // Configure your compilers
  compilers: {
    solc: {
      version: "0.8.0", // Fetch exact version from solc-bin
      settings: {          // See the solidity docs for advice about optimization and evmVersion
       optimizer: {
         enabled: false,
         runs: 200
       },
      }
    }
  },

  // Truffle DB is currently disabled by default; to enable it, set enabled: true
  db: {
    enabled: false
  }
};

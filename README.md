# TradeRES EU Blockchain Project

## Introduction

The TradeRES EU Blockchain Project is designed to revolutionize the energy sector by enabling secure, transparent, and efficient energy trading. Utilizing Ethereum blockchain technology, this project introduces two main smart contracts: `EnergyExchange` and `EnergyToken`. These contracts facilitate the production, consumption, and trading of energy tokens within a decentralized framework, promoting renewable energy usage and accessibility.

## Features

- **EnergyToken Contract**: Represents a digital token that mimics units of energy. The token is ERC-20 compliant, making it easily transferable and standardized across the Ethereum network.
- **EnergyExchange Contract**: Acts as the marketplace for energy tokens, allowing users to produce, consume, and trade energy tokens. It ensures secure transactions and maintains an accurate ledger of energy credits and debts.

## Installation

To get started with the TradeRES EU Blockchain Project, follow these steps:

1. **Install Node.js and npm**: Ensure you have Node.js and npm installed on your system. Visit [Node.js](https://nodejs.org/) for installation instructions.

2. **Install Truffle**: Truffle is a development environment, testing framework, and asset pipeline for blockchains using the Ethereum Virtual Machine (EVM). Install Truffle globally using npm:
    ```shell
    npm install -g truffle
    ```

3. **Clone the Repository**: Clone this repository to your local machine:
    ```shell
    git clone https://github.com/ocatak/TradeRES-BC-Portal
    ```

4. **Install Dependencies**: Navigate to the cloned repository folder and install the required npm packages:
    ```shell
    npm install
    ```

## Usage

### Compiling Contracts

Compile the smart contracts using Truffle:

```shell
truffle compile
```

### Deploying Contracts

Deploy the contracts to an Ethereum testnet (e.g., Rinkeby) using Truffle. Ensure you have a `.env` file with your Ethereum node URL and private key:

```shell
truffle migrate --network rinkeby
```

### Interacting with Contracts

Interact with the contracts through the Truffle console or by integrating them into a web application using `web3.js` or `ethers.js`.

Example of producing energy tokens:

```javascript
const energyExchange = await EnergyExchange.deployed();
energyExchange.produceEnergy(100, Date.now(), /* hour */);
```

## Contributing

Contributions to the TradeRES EU Blockchain Project are welcome! Here's how you can contribute:

- **Reporting Bugs**: Open an issue describing the bug and how to reproduce it.
- **Suggesting Enhancements**: Open an issue with your suggestions for improvements.
- **Pull Requests**: For substantial changes, please open an issue first to discuss what you would like to change. Ensure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Acknowledgements

- Ethereum and the Solidity language for enabling decentralized application development.
- The TradeRES EU project team and all contributors.

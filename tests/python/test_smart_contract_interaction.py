import json
import unittest
from web3 import Web3
from web3.middleware import geth_poa_middleware

class TestSmartContractInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Connect to local Ethereum node or testnet/mainnet through Infura
        cls.w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))  # Update this as needed
        cls.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # Ensure connection is successful
        assert cls.w3.isConnected(), "Failed to connect to Ethereum node."

        # Load contract ABI and bytecode (assuming you have them as JSON files or similar)
        with open('EnergyTokenABI.json', 'r') as abi_definition:
            cls.energy_token_abi = json.load(abi_definition)
        with open('EnergyTokenBytecode.json', 'r') as bytecode_definition:
            cls.energy_token_bytecode = json.load(bytecode_definition)['object']

        # Account setup
        cls.account = cls.w3.eth.accounts[0]  # Using the first account from Ganache or your Ethereum wallet
        cls.w3.eth.defaultAccount = cls.account  # Set the default account for transactions

    def deploy_contract(self):
        # Deploy the contract
        EnergyToken = self.w3.eth.contract(abi=self.energy_token_abi, bytecode=self.energy_token_bytecode)
        tx_hash = EnergyToken.constructor().transact()
        tx_receipt = self.w3.eth.waitForTransactionReceipt(tx_hash)
        return self.w3.eth.contract(address=tx_receipt.contractAddress, abi=self.energy_token_abi)

    def test_deploy_energy_token_contract(self):
        # Test deployment of the contract
        contract = self.deploy_contract()
        self.assertTrue(contract.address, "Contract deployment failed")

    def test_mint_tokens(self):
        # Test minting of tokens
        contract = self.deploy_contract()
        mint_amount = 1000
        contract.functions.mint(self.account, mint_amount).transact()
        balance = contract.functions.balanceOf(self.account).call()
        self.assertEqual(balance, mint_amount, "Minting tokens failed")

if __name__ == '__main__':
    unittest.main()

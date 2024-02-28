from web3 import Web3
import json
from solcx import compile_files
import solcx
import os

CONTRACT_ADDR_FILE = 'contract_address.txt'

# Connect to a local Ganache node
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
web3.eth.default_account = web3.eth.accounts[0]

def compile_contract(path, name):
    compiled_contacts = solcx.compile_files([path], solc_version='0.8.0')
    contract_interface = compiled_contacts['{}:{}'.format(path, name)]
    return contract_interface

# Compile the contract source code from the file
energy_exchange_contract_interface = compile_contract('./contracts/EnergyExchange.sol', 'EnergyExchange')
energy_token_contract_interface = compile_contract('./contracts/EnergyToken.sol', 'EnergyToken')

def get_contract_address(new_deployment = False):
    if new_deployment:
        os.remove(CONTRACT_ADDR_FILE)

    if os.path.exists(CONTRACT_ADDR_FILE):
        f = open(CONTRACT_ADDR_FILE,'r')
        energy_token_address = f.readline().strip()
        energy_exchange_address = f.readline().strip()
        print('energy_token_address \t:', energy_token_address)
        print('energy_exchange_address \t:', energy_exchange_address)
        f.close()
        
        energy_exchange_contract = web3.eth.contract(address=energy_exchange_address, abi=energy_exchange_contract_interface['abi'])
        energy_token_contract = web3.eth.contract(address=energy_token_address, abi=energy_token_contract_interface['abi'])
    else:
        energy_token_contract = web3.eth.contract(abi=energy_token_contract_interface['abi'], bytecode=energy_token_contract_interface['bin'])
        tx_hash = energy_token_contract.constructor(web3.eth.default_account).transact({'from': web3.eth.default_account, 'gas': 4100000})
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        energy_token_address = tx_receipt.contractAddress
        
        energy_exchange_contract = web3.eth.contract(abi=energy_exchange_contract_interface['abi'], bytecode=energy_exchange_contract_interface['bin'])
        tx_hash = energy_exchange_contract.constructor(energy_token_address).transact({'from': web3.eth.accounts[0], 'tokenAddress':web3.eth.accounts[0], 'gas': 4100000})
        tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
        energy_exchange_address = tx_receipt.contractAddress

        f = open(CONTRACT_ADDR_FILE,'w')
        f.write(energy_token_address + '\n')
        f.write(energy_exchange_address)
        f.close()

    return energy_token_address, energy_exchange_address, energy_exchange_contract, energy_token_contract

contract_address = get_contract_address(new_deployment = True)

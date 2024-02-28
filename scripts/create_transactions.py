from web3 import Web3
import pandas as pd

from deploy_contracts import get_contract_address

# Define the scale factor (e.g., 1e2 for two decimal places)
SCALE_FACTOR = 1

# Assuming you have the Web3 instance and default account set up as before
web3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
web3.eth.default_account = web3.eth.accounts[0]

energy_token_address, energy_exchange_address, energy_exchange_contract, energy_token_contract = get_contract_address()

# Read the Excel file
excel_path = './data/data.xlsx'  # Update with the correct path to your Excel file
xls = pd.ExcelFile(excel_path)

# Iterate over each sheet in the Excel file except 'Info'
for sheet_name in xls.sheet_names:
    if sheet_name == 'Info':
        continue  # Skip the 'Info' sheet

    # Read the sheet into a DataFrame
    df = pd.read_excel(xls, sheet_name=sheet_name)

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Extract date and hour information
        date = int(row['Date'].strftime('%Y%m%d'))  # Format the date as an integer yyyymmdd
        hour = int(row['Hour'])

        # Calculate the net energy balance for the row
        net_energy = row[2:].sum()  # Assuming the first two columns are 'Date' and 'Hour'

        # Convert the net energy to an integer representation using the scale factor
        scaled_net_energy = int(net_energy * SCALE_FACTOR)

        print('scaled_net_energy =====>', scaled_net_energy)

        # Build and send the transaction
        if net_energy > 0:  # Consumption
            try:
                consume_energy_call = energy_exchange_contract.functions.consumeEnergy(scaled_net_energy, date, hour).call({'from': web3.eth.default_account})
                print('consumeEnergy successful, result net_energy > 0:', consume_energy_call)
            except ValueError as e:
                print('Function call simulation failed with net_energy > 0:', e)
            '''
            consume_energy_txn = energy_exchange_contract.functions.consumeEnergy(scaled_net_energy, date, hour).build_transaction({
                'from': web3.eth.default_account,
                'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
                'gas': 41213
            })
            print('Transaction ====>', consume_energy_txn)
            tx_hash = web3.eth.send_transaction(consume_energy_txn)
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f'Energy consumed transaction receipt: {tx_receipt}')
            '''
        elif net_energy < 0:  # Production
            # Use the absolute value of scaled_net_energy for production
            scaled_net_energy = abs(scaled_net_energy)
            try:
                produce_energy_call = energy_exchange_contract.functions.produceEnergy(scaled_net_energy, date, hour).call({'from': web3.eth.default_account})
                print('produceEnergy successful, result net_energy < 0:', produce_energy_call)
            except ValueError as e:
                print('Function call simulation failed with net_energy < 0:', e)
            '''
            produce_energy_txn = energy_exchange_contract.functions.produceEnergy(abs(scaled_net_energy), date, hour).build_transaction({
                'from': web3.eth.default_account,
                'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
                'gas': 41213
            })
            tx_hash = web3.eth.send_transaction(produce_energy_txn)
            tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
            print(f'Energy produced transaction receipt: {tx_receipt}')
            '''

# Example of interacting with the contract: Producing Energy
amount_of_energy = 100  # Example amount
produce_energy_txn = energy_exchange_contract.functions.produceEnergy(amount_of_energy,1,1).build_transaction({
    'from': web3.eth.default_account,
    'nonce': web3.eth.get_transaction_count(web3.eth.default_account),
     'gas': 4100000
    # Additional transaction parameters like gas can be specified here
})
#signed_txn = web3.eth.account.sign_transaction(produce_energy_txn)
tx_hash = web3.eth.send_transaction(produce_energy_txn)
tx_receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
print(f'Energy produced transaction receipt: {tx_receipt}')

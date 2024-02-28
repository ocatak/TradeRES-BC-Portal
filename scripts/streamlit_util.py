import pandas as pd
import numpy as np

EXCEL_FILE_PATH = './data/Data.xlsx'
xls = pd.ExcelFile(EXCEL_FILE_PATH)

def get_user_count():
    # Return the number of tabs (sheets) in an Excel file, excluding the "info" sheet
    sheet_names = xls.sheet_names
    if 'Info' in sheet_names:
        sheet_names.remove('Info')
    return len(sheet_names), sheet_names

def get_the_num_of_meters():
    # Return the number of columns in all tabs (sheets) in an Excel file, excluding the "info" sheet
    total_columns = 0
    for sheet_name in xls.sheet_names:
        if sheet_name != 'Info':  # Skip the "info" sheet
            df = pd.read_excel(xls, sheet_name=sheet_name, nrows=1)  # Read only the first row to get the number of columns
            total_columns += len(df.columns)
    return total_columns

def create_hourly_balance_dataframe():
    # Create an empty DataFrame to store the hourly balance for each plant
    combined_df = pd.DataFrame()
    
    # Iterate through each sheet (plant)
    for sheet_name in xls.sheet_names:
        if sheet_name != 'Info':  # Skip the "info" sheet
            # Read the sheet data
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Convert 'Hour' column to integer dtype
            df['Hour'] = df['Hour'].astype(int)
            
            # Initialize dictionaries to store production, consumption, and balance for each hour
            production = {}
            consumption = {}
            balance = {}
            
            # Iterate through each hour of the day
            for hour in range(1,25):
                # Filter data for the current hour
                hour_data = df[df['Hour'] == hour]

                # Calculate average production and consumption for the hour, skipping the first two columns
                production[hour] = np.abs(hour_data.iloc[:, 2:][hour_data.iloc[:, 2:] < 0].mean().sum())
                consumption[hour] = hour_data.iloc[:, 2:][hour_data.iloc[:, 2:] > 0].mean().sum()
                
                # Replace NaN values with 0
                production[hour] = 0 if pd.isna(production[hour]) else production[hour]
                consumption[hour] = 0 if pd.isna(consumption[hour]) else consumption[hour]
                
                # Calculate balance for the hour
                balance[hour] = production[hour] - consumption[hour]
            
            # Create a DataFrame with 'Hour' as the index
            hour_index = pd.Index(range(1,25), name='Hour')
            df_hourly_balance = pd.DataFrame({'Balance': balance.values()}, index=hour_index)
            
            # Add the hourly balance DataFrame to the combined DataFrame with the plant name as the index
            combined_df[sheet_name] = df_hourly_balance#['Balance']
    
    return combined_df



def calculate_average_production_consumption():
    # Calculate average hourly production, consumption, and balance values for each sheet
    dfs = {}
    for sheet_name in xls.sheet_names:
        if sheet_name != 'Info':  # Skip the "info" sheet
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Convert 'Hour' column to integer dtype
            df['Hour'] = df['Hour'].astype(int)
            
            production = {}
            consumption = {}
            balance = {}
            for hour in range(24):
                hour_data = df[df['Hour'] == hour]
                
                # Check if any data exists for the current hour
                if not hour_data.empty:
                    # Calculate average production and consumption for the hour, skipping the first two columns
                    production[hour] = hour_data.iloc[:, 2:][hour_data.iloc[:, 2:] < 0].mean().mean()  
                    consumption[hour] = hour_data.iloc[:, 2:][hour_data.iloc[:, 2:] > 0].mean().mean()
                else:
                    production[hour] = 0  # Set production to 0 if no data exists
                    consumption[hour] = 0  # Set consumption to 0 if no data exists
                
                # Replace NaN values with 0
                production[hour] = 0 if pd.isna(production[hour]) else production[hour]
                consumption[hour] = 0 if pd.isna(consumption[hour]) else consumption[hour]
                
                # Calculate balance for the hour
                balance[hour] = production[hour] - consumption[hour]
            
            # Create a DataFrame with 'Hour' as the index
            hour_index = pd.Index(range(24), name='Hour')
            df_hourly = pd.DataFrame({'Production': production.values(), 
                                      'Consumption': consumption.values(), 
                                      'Balance': balance.values()}, index=hour_index)
            
            dfs[sheet_name] = df_hourly
    return dfs


def merge_production_consumption():
    # Read the entire Excel file into memory
    all_data = pd.read_excel(EXCEL_FILE_PATH, sheet_name=None)
    
    # Initialize an empty dictionary to store merged production and consumption data for each plant
    merged_data = {}
    
    # Iterate through each sheet (plant)
    for sheet_name, df in all_data.items():
        if sheet_name != 'Info':  # Skip the "info" sheet
            # Initialize an empty list to store merged production and consumption data for each hour for the current plant
            plant_data = []
            
            # Iterate through each hour (1 to 24)
            for hour in range(1, 25):
                # Filter data for the current hour
                hour_data = df[df['Hour'] == hour]
                
                # Extract columns with negative values as production and positive values as consumption
                production_columns = hour_data.iloc[:, 2:][hour_data.iloc[:, 2:] < 0].fillna(0)
                consumption_columns = hour_data.iloc[:, 2:][hour_data.iloc[:, 2:] > 0].fillna(0)
                
                # Calculate mean production and consumption for the current hour
                production_mean = production_columns.mean().mean()
                consumption_mean = consumption_columns.mean().mean()
                
                # Calculate lower and upper bound (sigma) for production and consumption
                production_sigma = production_columns.stack().std()
                consumption_sigma = consumption_columns.stack().std()
                
                # Create a DataFrame with data for the current hour
                hour_df = pd.DataFrame({
                    'Hour': hour,
                    'Average_Production': production_mean,
                    'Average_Consumption': consumption_mean,
                    #'Production_Lower_Bound': production_mean - production_sigma,
                    #'Production_Upper_Bound': production_mean + production_sigma,
                    #'Consumption_Lower_Bound': consumption_mean - consumption_sigma,
                    #'Consumption_Upper_Bound': consumption_mean + consumption_sigma
                }, index=[0])  # Create DataFrame with single row
                hour_df['Production_Lower_Bound'] = hour_df['Average_Production'] - production_sigma
                hour_df['Production_Upper_Bound'] = hour_df['Average_Production'] + production_sigma
                hour_df['Consumption_Lower_Bound'] = hour_df['Average_Consumption'] - consumption_sigma
                hour_df['Consumption_Upper_Bound'] = hour_df['Average_Consumption'] + consumption_sigma
                
                # Append the DataFrame to the list for the current plant
                plant_data.append(hour_df)
            
            # Concatenate all DataFrames in the list to form the final DataFrame for the current plant
            merged_data[sheet_name] = pd.concat(plant_data, ignore_index=True)
    
    return merged_data





def get_last_hour_balance():
    # Initialize dictionary to store last hour balance for each plant
    last_hour_balances = {}
    
    # Iterate through each sheet (plant)
    for sheet_name in xls.sheet_names:
        if sheet_name != 'Info':  # Skip the "info" sheet
            # Read the sheet data
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Convert 'Hour' column to integer dtype
            df['Hour'] = df['Hour'].astype(int)

            # Filter data for the last hour of the last day
            last_hour_data = df[(df['Date'] == df['Date'].max()) & (df['Hour'] == df['Hour'].max())]
            
            # Calculate production and consumption for the last hour
            production = np.abs(last_hour_data.iloc[:, 2:][last_hour_data.iloc[:, 2:] < 0].sum().sum())
            consumption = last_hour_data.iloc[:, 2:][last_hour_data.iloc[:, 2:] > 0].sum().sum()
            
            # Replace NaN values with 0
            production = 0 if pd.isna(production) else production
            consumption = 0 if pd.isna(consumption) else consumption
            
            # Calculate balance for the last hour
            balance = production - consumption
            
            # Store the last hour balance for the current plant
            last_hour_balances[sheet_name] = balance
    
    # Convert the dictionary to a pandas DataFrame
    last_hour_df = pd.DataFrame(last_hour_balances.values(), index=last_hour_balances.keys(), columns=['Last Hour Balance'])
    
    return last_hour_df

def get_last_24_hour_data():
    # Initialize a dictionary to store the dataframes for each sheet
    last_24_hour_data = {}
    
    # Iterate through each sheet (plant)
    for sheet_name in xls.sheet_names:
        if sheet_name != 'Info':  # Skip the "info" sheet
            # Read the sheet data
            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            # Get the last 24 hours of data
            last_24_hours_df = df.tail(24)
            
            # Sum the consumption and production for each hour
            hourly_consumption = last_24_hours_df.iloc[:, 2:][last_24_hours_df.iloc[:, 2:] > 0].sum(axis=0)
            hourly_production = np.abs(last_24_hours_df.iloc[:, 2:][last_24_hours_df.iloc[:, 2:] < 0]).sum(axis=1)
            
            # Create a DataFrame with hourly consumption and production
            hourly_data_df = pd.DataFrame({'Hourly_Consumption': hourly_consumption, 'Hourly_Production': hourly_production})
            hourly_data_df.index.name = 'Hour'
            
            # Store the DataFrame for the current sheet
            last_24_hour_data[sheet_name] = hourly_data_df
    
    return last_24_hour_data



if __name__ == '__main__':
    #print(calculate_average_production_consumption())
    print(get_last_24_hour_data())
    #print(create_hourly_balance_dataframe())

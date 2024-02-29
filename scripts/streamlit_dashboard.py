# streamlit run scripts/streamlit_dashboard.py 
import streamlit as st
from streamlit_util import *  # Import the new method
import pydeck as pdk

import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(
    page_title="Real-Time TradeRES Dashboard",
    page_icon="✅",
    layout="wide",
)

# 
num_of_plants, plant_names = get_user_count()

#######################
# Calculate the required width for each column based on content
widths = [10, 300 ,100, 100,10]  # Set the initial widths for each column

# Determine the maximum width required for each column
max_widths = [max(width, 100) for width in widths]  # Ensure a minimum width of 100 pixels

# Load the logo image
logo = "./scripts/TradeRES-59.svg"

col1, col2, col3, col4, col5 = st.columns(max_widths)
# Display the logo
col1.image(logo, use_column_width=True)  # Adjust the size of the logo to fit the column width

# Streamlit app
col2.write('# TradeRES Data Dashboard')

col3.metric("Clients", f"{num_of_plants}", delta=0, delta_color="inverse")
col4.metric("Smart Meters", f"{get_the_num_of_meters()}", delta=0, delta_color="inverse")
col5.image("./scripts/GitHub-logo.png")
col5.write("[GitHub Repository](https://github.com/ocatak/TradeRES-BC-Portal/)", unsafe_allow_html=True)



# Display the raw data
# st.subheader('Raw Data from Ethereum Smart Contract')

st.write(":heavy_minus_sign:" * 80)  # horizontal separator line.

# KPI values# Create columns for each gauge plot
last_hour_balance_df = get_last_hour_balance()
st.write("## Last Hour Balance")  # horizontal separator line.

columns = st.columns(len(last_hour_balance_df))


# Add gauges for each plant to the Plotly figure
for i, (plant, balance) in enumerate(last_hour_balance_df.iterrows()):
    with columns[i]:
        st.plotly_chart(
            go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=balance['Last Hour Balance'],
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': f"{plant}"},
                    gauge={
                        'axis': {'range': [last_hour_balance_df.min().values[0]*1.1, last_hour_balance_df.max().values[0]*1.1]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [last_hour_balance_df.min().values[0], 0], 'color': "red"},
                            {'range': [0, last_hour_balance_df.max().values[0]], 'color': "green"}
                        ]
                    }
                )
            ),
            use_container_width=True,use_container_height=True  # Dynamically adjust the width based on available space
        )

# Display the hourly balance DataFrame
hourly_balance_df = merge_production_consumption()  # Call the method to get merged production and consumption data

columns = st.columns(len(hourly_balance_df))
for (i,plant_name) in zip(range(len(plant_names)),plant_names):
    hourly_balance_plant_df = hourly_balance_df[plant_name]  # Get the hourly balance for the current plant
    with columns[i]:
        # Plot production and consumption for each plant
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=hourly_balance_plant_df['Hour'], y=hourly_balance_plant_df['Average_Production'], mode='lines', line=dict(width=1.5, color="rgb(255, 188, 0)"), name=f'Avg Production'))
        #fig.add_trace(go.Scatter(x=hourly_balance_plant_df['Hour'], y=hourly_balance_plant_df['Production_Upper_Bound'], mode='lines', line=dict(width=0.2, color="rgb(255, 188, 0)"), fillcolor='rgba(68, 68, 68, 0.1)', fill='toself', name=f'Upper bound prod'))
        #fig.add_trace(go.Scatter(x=hourly_balance_plant_df['Hour'], y=hourly_balance_plant_df['Production_Lower_Bound'], mode='lines', line=dict(width=0.2, color="rgb(141, 196, 0)"), name=f'Lower bound avg'))

        fig.add_trace(go.Scatter(x=hourly_balance_plant_df['Hour'], y=hourly_balance_plant_df['Average_Consumption'], mode='lines', line=dict(width=1.5, color="rgb(0, 188, 0)"), name=f'Consumption'))
        #fig.add_trace(go.Scatter(x=hourly_balance_plant_df['Hour'], y=hourly_balance_plant_df['Consumption_Upper_Bound'], mode='lines', line=dict(width=0.2, color="rgb(255, 188, 0)"), fillcolor='rgba(68, 68, 68, 0.1)', fill='toself', name=f'Upper bound cons'))
        #fig.add_trace(go.Scatter(x=hourly_balance_plant_df['Hour'], y=hourly_balance_plant_df['Consumption_Lower_Bound'], mode='lines', line=dict(width=0.2, color="rgb(141, 196, 0)"), fillcolor='rgba(68, 68, 68, 0.1)', name=f'Lower bound avg'))



        fig.update_layout( title=f'{plant} by Hour',
                            xaxis_title='Hour',
                            yaxis_title='Value',
                            legend=dict(
                                orientation="h",
                                yanchor="bottom",
                                y=1.02,
                                xanchor="left",
                                x=0
                            ),
                            xaxis=dict(
                                title='Hour',
                                tickmode='linear',
                                dtick=2,
                                gridcolor='rgba(0,0,0,0.1)'
                            ),
                            yaxis=dict(
                                title='Value',
                                gridcolor='rgba(0,0,0,0.1)'
                            )
                        )

        st.plotly_chart(fig, use_container_width=True)

# Display the hourly balance DataFrame
hourly_balance_df = create_hourly_balance_dataframe()  # Call the new method

# Display KPIs horizontally
st.write(":heavy_minus_sign:" * 80)  # horizontal separator line.

# Calculate the required width for each column based on content
widths = [100, 100, 1200]  # Set the initial widths for each column

# Determine the maximum width required for each column
max_widths = [max(width, 100) for width in widths]  # Ensure a minimum width of 100 pixels

col1, col2, col3 = st.columns(max_widths)
col1.metric("Clients", f"{num_of_plants}", delta=0, delta_color="inverse")
col2.metric("Smart Meters", f"{get_the_num_of_meters()}", delta=0, delta_color="inverse")
col3.table(hourly_balance_df.T)

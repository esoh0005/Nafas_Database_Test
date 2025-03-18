import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Database name
DB_NAME = "nafas.db"

# Mapping of state IDs to names
state_mapping = {
    1: "Kuala Lumpur",
    2: "Selangor",
    3: "Putrajaya",
    4: "Melaka",
    5: "Negeri Sembilan",
    6: "Johor",
    7: "Perak",
    8: "Kedah",
    9: "Perlis",
    10: "Penang",
    11: "Pahang",
    12: "Kelantan",
    13: "Terengganu",
    14: "Sabah",
    15: "Sarawak",
}

# Function to connect to the database
def get_connection():
    conn = sqlite3.connect(DB_NAME)
    return conn

# Function to get table names
def get_table_names():
    conn = get_connection()
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql(query, conn)
    conn.close()
    return tables['name'].tolist()

# Function to fetch filtered data
def fetch_filtered_data(table_name, state_id=None):
    conn = get_connection()
    
    if table_name == "prevalence_incidence_asthma":
        query = f"SELECT * FROM {table_name} LIMIT 100;"
    elif table_name == "aqi_yearly_state":
        query = f"SELECT * FROM {table_name} WHERE state_id = {state_id};"
    else:
        query = f"SELECT * FROM {table_name} WHERE state_id = {state_id} ORDER BY date ASC;"
    
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Function to plot AQI Yearly data
def plot_aqi_yearly(df):
    if df.empty:
        return
    fig, ax = plt.subplots()
    ax.plot(df["year"], df["aqi"], marker="o", linestyle="-", label="AQI")
    ax.set_xlabel("Year")
    ax.set_ylabel("AQI")
    ax.set_title("AQI Yearly Trend")
    ax.legend()
    st.pyplot(fig)

# Streamlit UI
st.title("Nafas Database Viewer")
st.markdown("### Browse and explore the imported CSV data")

# Dropdown to select a table
table_names = get_table_names()

if table_names:
    selected_table = st.selectbox("Select a dataset", table_names)

    # Show state filter only for AQI and Weather datasets
    if selected_table in ["aqi_yearly_state", "combined_aqi_data", "combined_weather_data"]:
        selected_state = st.selectbox("Select a state", list(state_mapping.values()))
        state_id = [key for key, value in state_mapping.items() if value == selected_state][0]
    else:
        state_id = None  # No filter for prevalence_incidence_asthma

    # Load data button
    if st.button("Load Data"):
        df = fetch_filtered_data(selected_table, state_id)

        if df.empty:
            st.warning(f"No data found for {selected_table}.")
        else:
            st.write(f"Showing data for **{selected_table}**")
            st.dataframe(df)

            # Plot AQI Yearly Trend (Only for aqi_yearly_state)
            if selected_table == "aqi_yearly_state":
                plot_aqi_yearly(df)
else:
    st.warning("No tables found in the database. Make sure the CSV files have been imported.")

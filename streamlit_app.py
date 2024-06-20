import streamlit as st 
import pandas as pd
from datetime import datetime, time
import datetime as dt
import pytz

st.set_page_config(page_title="Cellserv Tracking - Kookee Enterprises Dashboard", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
st.markdown("UAN 020N and UAW 109Z")

st.write("A breakdown of locations visited by UAN 020N and UAW 109Z ")

# Initialize connection.
conn = st.connection("postgresql", type="sql")
q = """SELECT vehicle, st_d_time, start_address, start_coordinate, ed_d_time, end_address, end_coordinate, total_distance_km, d_duration FROM workdesk_ridereport WHERE d_duration < '5 hours' ORDER BY st_d_time DESC"""
# Perform query.
dft = conn.query(q, ttl="10m")

dfb = pd.DataFrame(dft)
counts = dfb['start_address'].value_counts()
print(counts)
st.write("Most Visited Locations")
st.dataframe(counts)

#Sidebar
with st.sidebar:
#Date Range Filter
    start_date = st.date_input('Start date', value=dt.date(2023, 6, 1))
    end_date = st.date_input('End date', value=dt.date(2024,2,29))

    # Dropdown for filtering Vehicle
    category = st.selectbox('Select a vehicle:', dfb['vehicle'].unique())

# Convert start_date and end_date to datetime objects with a timezone
start_datetime = datetime.combine(start_date, time()).replace(tzinfo=pytz.utc)
end_datetime = datetime.combine(end_date, time()).replace(tzinfo=pytz.utc)

# Filter data
filtered_df = dfb[(dfb['st_d_time'] >= start_datetime) & (dfb['st_d_time'] <= end_datetime) & (dfb['vehicle'] == category)]
count_df = filtered_df['start_address'].value_counts()


st.write("Results By Date and Vehicle")

# Create a dictionary to map start_address to start_coordinate
address_to_coordinate = dfb.set_index('start_address')['start_coordinate'].to_dict()

# Create a new column in count_df with the mapped start_coordinates
count_df['start_coordinate'] = count_df.index.map(address_to_coordinate)

# Reset the index to get a clean dataframe
count_df = count_df.reset_index()

st.dataframe(count_df, column_config={
    "vehicle": "Vehicle",
    "start_address": "Start Address",
    "start_coordinate": "GPS Coordinates",
    "count": "Visits"})

st.dataframe(dft, column_config={
        "vehicle": "Vehicle",
        "st_d_time": "Start Time",
        "start_address": "Start Address",
        "ed_d_time": "End Time",
        "end_address": "End Address",
        "total_distance_km": "Distance Travelled",
        "d_duration": "Travel Duration"
        })        


st.write("Here we are at the end of getting started with streamlit! Happy Streamlit-ing! :balloon:")
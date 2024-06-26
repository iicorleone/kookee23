import streamlit as st 
import pandas as pd
from datetime import datetime, time
import datetime as dt
import pytz

st.set_page_config(page_title="Cellserv Tracking - Kookee Enterprises Dashboard", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)


# Initialize connection.
conn = st.connection("postgresql", type="sql")
q = """SELECT vehicle, st_d_time, start_address, start_coordinate, ed_d_time, end_address, end_coordinate, total_distance_km, d_duration FROM workdesk_ridereport WHERE d_duration < '5 hours' ORDER BY st_d_time DESC"""
# Perform query.
dft = conn.query(q, ttl="10m")

dfb = pd.DataFrame(dft)
counts = dfb['start_address'].value_counts()
st.write("Most Visited Locations")
# st.dataframe(counts)

#Sidebar
with st.sidebar:
    st.markdown("UAN 020N and UAW 109Z")

    st.write("A breakdown of locations visited by UAN 020N and UAW 109Z")
    st.write("Select suitable dates or vehicle to see results for specific dates or vehicle")
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


st.write(f"""Results from {start_date} to {end_date} for Vehicle {category}""")

# Create a dictionary to map start_address to start_coordinate
address_to_coordinate = dfb.set_index('start_address')['start_coordinate'].to_dict()

# Create a new dataframe with the mapped address_to_coordinate dictionary
coordinate_df = pd.DataFrame({'start_address': list(address_to_coordinate.keys()), 
                              'start_coordinate': list(address_to_coordinate.values())})

# Merge the coordinate_df with count_df
merged_df = pd.merge(coordinate_df, count_df, on='start_address')

# Create a new column in count_df with the mapped start_coordinates
count_df['start_coordinate'] = count_df.index.map(address_to_coordinate)

# Reset the index to get a clean dataframe
count_df = count_df.reset_index()
# Define a function to create the Google Maps URL
# Define a function to create a clickable Google Maps URL
# def create_clickable_google_maps_url(row):
#     coordinates = row['start_coordinate']
#     coordinates = coordinates.strip('[]')  # Remove square brackets
#     latitude, longitude = coordinates.split(',')  # Split into two values
#     url = f"https://www.google.com/maps/search/?api=1&query={longitude}%2C{latitude}"
#     link = f"<a href='{url}' target='_blank'>View on Google Maps</a>"
#     return link

# # Apply the function to each row in merged_df
# merged_df['google_maps_url'] = merged_df.apply(create_clickable_google_maps_url, axis=1)

# st.dataframe(merged_df,
#              column_config={
#     "start_address": "Address",
#     "start_coordinate": "GPS Coordinates",
#     "google_maps_url": "Google Maps Link (Click to Open Location)",
#     "count": "Visits"}
# )

# # Render the HTML links
# for index, row in merged_df.iterrows():
#     st.write(f"{row['google_maps_url']}", unsafe_allow_html=True)

# Define a function to create a clickable Google Maps URL
def create_clickable_google_maps_url(row):
    coordinates = row['start_coordinate']
    coordinates = coordinates.strip('[]')  # Remove square brackets
    latitude, longitude = coordinates.split(',')  # Split into two values
    url = f"https://www.google.com/maps/search/?api=1&query={longitude}%2C{latitude}"
    link = f"""<a href="{url}">[View on Google Maps]</a>"""
    return url

# Apply the function to each row in merged_df
merged_df['google_maps_url'] = merged_df.apply(create_clickable_google_maps_url, axis=1)
st.dataframe(merged_df, column_config={
        "google_maps_url": st.column_config.LinkColumn("Click to Open Location on Google"),
        "start_address" : "Address",
        "start_coordinate" : "GPS Coordinates",
        "count" : "Visits"
    })

# # Create a Streamlit dataframe with Markdown enabled
# st.write(merged_df.style.format({"google_maps_url": lambda x: x}), width=1000)

# Render the dataframe as Markdown
# st.markdown(merged_df.to_markdown(index=False, tablefmt="grid"), unsafe_allow_html=True)

# st.dataframe(dft, column_config={
#         "vehicle": "Vehicle",
#         "st_d_time": "Start Time",
#         "start_address": "Start Address",
#         "ed_d_time": "End Time",
#         "end_address": "End Address",
#         "total_distance_km": "Distance Travelled",
#         "d_duration": "Travel Duration"
#         })        


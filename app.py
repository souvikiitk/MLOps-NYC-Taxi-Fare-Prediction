import streamlit as st
import folium as fl
from streamlit_folium import st_folium
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import pickle
from math import sin, asin, cos, sqrt, radians
# from utils.helper import haversine_dist

# # Using object notation
# add_selectbox = st.sidebar.selectbox(
#     "How would you like to be contacted?",
#     ("Email", "Home phone", "Mobile phone")
# )


def haversine_dist(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose an option",
        ("Calculate Taxi fare", "DataSet Description")
    )

if add_radio == "Calculate Taxi fare":
    key_locations = {
        "CentralPark": [40.7826, -73.9656],
        "Times Square": 	[40.758896, -73.985130],
        "World Trade Center": [40.7127, -74.0134],
        "New York University": [40.729675, -73.996925],
        "Columbia University": [40.8075, -73.9626],
        "Rutgers University": [40.5018, -74.4479],
        "Wall Street": [40.7069, -74.0113],
        "Madison Square Garden": [40.7505, -73.9934],
        "Broadway theatre": [40.7632, -73.9831],
        "Yankee Stadium": [40.8296, -73.9262],
        "Museum of Modern Art": [40.7614, -73.9776],
        "Chinatown": [40.7158, -73.9970],
        "Federal Reserve Bank of New York": [40.7084, -74.0087]}

    st.title('Taxi fare in New York City')

    # Initialize session state
    if "pickup_lat" not in st.session_state:
        st.session_state.pickup_lat = None
        st.session_state.pickup_lon = None
        st.session_state.dropoff_lat = None
        st.session_state.dropoff_lon = None
        st.session_state.passenger_count = 1

    # Initialize the DataFrame
    test_check = pd.DataFrame({
        "pickup_longitude": [],
        "pickup_latitude": [],
        "dropoff_longitude": [],
        "dropoff_latitude": [],
        "passenger_count": [],
        "distance_km": []
    })

    # Step 1: Select Pickup Location
    if st.session_state.pickup_lat is None:
        st.subheader("Select Pickup Location")
        m = fl.Map(tiles="OpenStreetMap", zoom_start=11, location=[
                   40.78910688411592, -73.98452568420909])
        m.add_child(fl.LatLngPopup())
        map_ny = st_folium(m, height=400, width=700)

        if map_ny["last_clicked"]:
            st.session_state.pickup_lat = map_ny["last_clicked"]["lat"]
            st.session_state.pickup_lon = map_ny["last_clicked"]["lng"]
            st.rerun()  # Rerun to move to the next step

    # Step 2: Select Drop-off Location
    if st.session_state.pickup_lat is not None and st.session_state.dropoff_lat is None:
        st.subheader("Select Drop-off Location")
        m = fl.Map(tiles="OpenStreetMap", zoom_start=11, location=[
                   40.78910688411592, -73.98452568420909])
        fl.Marker([st.session_state.pickup_lat, st.session_state.pickup_lon],
                  popup="Pickup Location").add_to(m)
        m.add_child(fl.LatLngPopup())
        map_ny = st_folium(m, height=400, width=700)

        if map_ny["last_clicked"]:
            st.session_state.dropoff_lat = map_ny["last_clicked"]["lat"]
            st.session_state.dropoff_lon = map_ny["last_clicked"]["lng"]
            st.rerun()  # Rerun to move to the next step

    # Step 3: Input Number of Passengers
    if st.session_state.pickup_lat is not None and st.session_state.dropoff_lat is not None:
        st.subheader("Input Number of Passengers")
        st.session_state.passenger_count = st.number_input(
            "Number of Passengers", min_value=1, value=1, step=1)

        # Display the selected locations and passenger count
        st.write(f"Pickup Location: Latitude: {st.session_state.pickup_lat}, Longitude: {st.session_state.pickup_lon}")
        st.write(f"Drop-off Location: Latitude: {st.session_state.dropoff_lat}, Longitude: {st.session_state.dropoff_lon}")
        st.write(f"Number of Passengers: {st.session_state.passenger_count}")

        # Calculate and display distance
        pickup_coords = (st.session_state.pickup_lat,
                         st.session_state.pickup_lon)
        dropoff_coords = (st.session_state.dropoff_lat,
                          st.session_state.dropoff_lon)
        distance = geodesic(pickup_coords, dropoff_coords).km
        st.write(f"Distance between pickup and drop-off: {distance:.2f} km")

        # Create a new DataFrame row
        new_row = pd.DataFrame({
            "pickup_longitude": [st.session_state.pickup_lon],
            "pickup_latitude": [st.session_state.pickup_lat],
            "dropoff_longitude": [st.session_state.dropoff_lon],
            "dropoff_latitude": [st.session_state.dropoff_lat],
            "passenger_count": [st.session_state.passenger_count],
            "distance_km": [distance]
        })

        # for key in key_locations.keys():
        #     new_row[key + '_distance_km'] = new_row.apply(lambda row: haversine_dist(row['pickup_longitude'], row['pickup_latitude'],
                                                                                    #  key_locations[key][1], key_locations[key][0]), axis=1)

        if st.button("Reset"):
            st.session_state.pickup_lat = None
            st.session_state.pickup_lon = None
            st.session_state.dropoff_lat = None
            st.session_state.dropoff_lon = None
            st.session_state.passenger_count = 1
            st.rerun()

        # Concatenate the new row to the existing DataFrame
        test_check = pd.concat([test_check, new_row], ignore_index=True)

        st.subheader("Collected Data")
        st.dataframe(test_check)

        # test_check[key + '_distance_km'] = test_check.apply(lambda row: haversine_dist(row['pickup_longitude'], row['pickup_latitude'],
                                                                                    #    key_locations[key][1], key_locations[key][0]), axis=1)

        if st.button("Calculate Fare"):
            with open('models/model.pkl', 'rb') as file:
                loaded_model = pickle.load(file)
            print(new_row)
            fare_value = loaded_model.predict(new_row)
            st.subheader("Here is your Fare")
            st.write(f"Taxi Value: {fare_value[0]}")

if add_radio == "DataSet Description":
    st.title("DataSet Description")

    # Load the data from the CSV file
    location_cols = ["pickup_longitude", "pickup_latitude"]
    # df = pd.read_csv("./uber-fares-dataset/uber.csv", usecols=location_cols)
    df = pd.read_csv("./dataset/uber.csv", usecols=location_cols, nrows=2000)
    df.rename(columns = {"pickup_longitude": "LON", "pickup_latitude": "LAT"}, inplace=True)
    # Display the first few rows of the dataframe (optional)
    st.write("Data Preview:")

    # Create a map using the latitude and longitude data
    st.map(df)
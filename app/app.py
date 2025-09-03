import streamlit as st
import pickle
from zenml.client import Client
import pandas as pd

# Get latest pipeline run
client = Client()
pipeline_run = client.get_pipeline("your_pipeline_name").last_successful_run

# Access the model step's output
model_bytes = pipeline_run.get_step("train_model").output["output"].read()

# Load model
model = pickle.loads(model_bytes)

# Streamlit interface
st.title("NYC Taxi Fare Predictor")

# Input form
pickup_long = st.number_input("Pickup Longitude", value=-73.985428)
pickup_lat = st.number_input("Pickup Latitude", value=40.748817)
dropoff_long = st.number_input("Dropoff Longitude", value=-73.985428)
dropoff_lat = st.number_input("Dropoff Latitude", value=40.748817)
passenger_count = st.slider("Passenger Count", 1, 6, 1)

if st.button("Predict Fare"):
    # Create input DataFrame
    input_df = pd.DataFrame([{
        "pickup_longitude": pickup_long,
        "pickup_latitude": pickup_lat,
        "dropoff_longitude": dropoff_long,
        "dropoff_latitude": dropoff_lat,
        "passenger_count": passenger_count,
        "distance_km": 1.5  # (calculate manually or reuse your logic)
    }])
    prediction = model.predict(input_df)
    st.success(f"Predicted Fare: ${prediction[0]:.2f}")

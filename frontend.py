# frontend.py
import streamlit as st
import requests

st.title("PyTorch Model Inference")
st.write("Enter input features as comma-separated values.")

# Input field for features
input_str = st.text_input("Input (e.g., 0.5, 1.2, -0.3, ...)", "")

if st.button("Predict"):
    try:
        # Process input: convert comma-separated string to list of floats
        input_data = [float(x.strip()) for x in input_str.split(",") if x.strip() != ""]
        # Call the Flask API (adjust URL if needed)
        response = requests.post("http://localhost:5000/predict", json={"input": input_data})
        if response.status_code == 200:
            st.success(f"Prediction: {response.json()['prediction']}")
        else:
            st.error(f"Error: {response.json().get('error')}")
    except Exception as e:
        st.error(f"Invalid input or request error: {e}")

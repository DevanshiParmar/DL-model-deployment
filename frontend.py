# frontend.py
import streamlit as st
import requests
from PIL import Image
import io
import pandas as pd

# Define class mapping
class_map = {0: "Dog", 1: "Food", 2: "Vehicle"}

st.title("ResNet18 Image Classification")
st.write("Upload an image (expected size: 3x64x64) for classification. The classes are: Dog, Food, and Vehicle.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image')
    
    if st.button("Predict"):
        # Convert image to bytes
        buf = io.BytesIO()
        image.save(buf, format='PNG')
        buf.seek(0)
        files = {"file": ("image.png", buf, "image/png")}
        
        try:
            # Update the URL below if your backend is hosted elsewhere
            response = requests.post("http://localhost:5000/predict", files=files)
            if response.status_code == 200:
                result = response.json()
                pred_class = result['prediction']
                probabilities = result['probabilities']
                
                # Display the predicted class with a friendly label
                st.success(f"Prediction: {class_map.get(pred_class, 'Unknown')}")
                
                # Create a DataFrame for probabilities
                prob_df = pd.DataFrame({
                    "Class": ["Dog", "Food", "Vehicle"],
                    "Probability": probabilities
                })
                st.write("Class Probabilities:")
                st.bar_chart(prob_df.set_index("Class"))
            else:
                st.error(f"Error: {response.json().get('error')}")
        except Exception as e:
            st.error(f"Request failed: {e}")

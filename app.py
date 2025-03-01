# app.py
from flask import Flask, request, jsonify
import torch
import io
from PIL import Image
import torchvision.transforms as transforms

app = Flask(__name__)

# Load the latest serialized model
model = torch.jit.load("serialized_models/model_v1.pt")
model.eval()

# Define image preprocessing: resize to 64x64, convert to tensor, and normalize to [-1, 1]
preprocess = transforms.Compose([
    transforms.Resize((64, 64)),                # Ensure the image is 64x64
    transforms.ToTensor(),                      # Convert PIL image to tensor in [0,1]
    transforms.Normalize(mean=[0.5, 0.5, 0.5],    # Normalize to [-1,1]
                         std=[0.5, 0.5, 0.5]),
])

@app.route("/predict", methods=["POST"])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file part in the request"}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected for uploading"}), 400
        
        # Read and preprocess the image
        img_bytes = file.read()
        img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        input_tensor = preprocess(img).unsqueeze(0)  # add batch dimension

        with torch.no_grad():
            output = model(input_tensor)
        
        # Get predicted class and probabilities
        prediction = torch.argmax(output, dim=1).item()
        probabilities = torch.softmax(output, dim=1).squeeze().tolist()

        return jsonify({"prediction": prediction, "probabilities": probabilities})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

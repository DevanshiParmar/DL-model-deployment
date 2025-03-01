# app.py
from flask import Flask, request, jsonify
import torch

app = Flask(__name__)

# Load the serialized model
model = torch.jit.load("serialized_models/model_v1.pt")
model.eval()

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)
        # Expecting a key 'input' with a list of numbers
        input_data = data.get("input")
        if input_data is None:
            return jsonify({"error": "No input data provided"}), 400

        # Convert input to a torch tensor (assumes input is 1D list for a single sample)
        input_tensor = torch.tensor(input_data, dtype=torch.float32).unsqueeze(0)
        with torch.no_grad():
            output = model(input_tensor)
        prediction = output.numpy().tolist()
        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# app.py
import os
import io
import base64
from flask import Flask, render_template, request, redirect, url_for, flash
import torch
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key

# Get the model filename from the environment (default to "model_latest.pt")
model_file = os.environ.get("MODEL_FILE", "model_latest.pt")
model = torch.jit.load(model_file)
model.eval()

# Define image preprocessing: resize to 64x64, convert to tensor, and normalize to [-1, 1]
preprocess = transforms.Compose([
    transforms.Resize((64, 64)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
])

# Define class mapping
class_map = {0: "Dog", 1: "Food", 2: "Vehicle"}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part")
            return redirect(request.url)
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file:
            try:
                # Read the image bytes and open with PIL
                img_bytes = file.read()
                original_img = Image.open(io.BytesIO(img_bytes)).convert("RGB")
                
                # Convert the original image to a base64 string for display
                buffered_img = io.BytesIO()
                original_img.save(buffered_img, format="PNG")
                uploaded_image_b64 = base64.b64encode(buffered_img.getvalue()).decode('utf-8')
                
                # Preprocess the image and predict
                input_tensor = preprocess(original_img).unsqueeze(0)
                with torch.no_grad():
                    output = model(input_tensor)
                prediction = torch.argmax(output, dim=1).item()
                probabilities = torch.softmax(output, dim=1).squeeze().tolist()
                
                # Create a bar chart of probabilities with the highest one highlighted
                classes_list = ["Dog", "Food", "Vehicle"]
                fig, ax = plt.subplots()
                max_index = probabilities.index(max(probabilities))
                colors = ["red" if i == max_index else "blue" for i in range(len(probabilities))]
                ax.bar(classes_list, [p * 100 for p in probabilities], color=colors)
                ax.set_ylabel("Probability (%)")
                ax.set_title("Predicted Class Probabilities")
                
                buf = io.BytesIO()
                plt.savefig(buf, format="png", bbox_inches="tight")
                buf.seek(0)
                probability_graph = base64.b64encode(buf.getvalue()).decode("utf-8")
                plt.close(fig)
                
                return render_template("result.html", 
                                       prediction=class_map.get(prediction, "Unknown"),
                                       probabilities=probabilities,
                                       classes=classes_list,
                                       uploaded_image=uploaded_image_b64,
                                       probability_graph=probability_graph,
                                       zip=zip)
            except Exception as e:
                flash(f"Error processing image: {e}")
                return redirect(request.url)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY serialized_models/ serialized_models/
COPY templates/ templates/

EXPOSE 5000

ENV MODEL_FILE=serialized_models/model_v1.pt

CMD ["python", "app.py"]

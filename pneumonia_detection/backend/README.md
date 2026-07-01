# Pneumonia Detection API

FastAPI backend serving a ResNet50-based Keras model for pneumonia classification
from chest X-ray images.

## Setup

1. Place your trained model file at `model/pneumonia_resnet50.h5`
   (or update `MODEL_PATH` in `app.py` to point to your actual file).

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run locally:
   ```
   uvicorn app:app --reload
   ```
   API will be live at `http://localhost:8000`.

## Endpoints

- `GET /health` — check if the API and model are up
- `POST /predict` — send an image file (`multipart/form-data`, field name `file`), returns:
  ```json
  { "label": "Pneumonia", "confidence": 92.4, "raw_score": 0.924 }
  ```

## Before deploying

- Double-check `MODEL_PATH` and that class 1 (`pred > 0.5`) actually corresponds
  to "Pneumonia" in your training generator's `class_indices` — flip the logic
  in `predict()` if it's inverted.
- Replace `allow_origins=["*"]` in the CORS config with your real frontend URL.
- If your `.h5` file is large, cold starts on free-tier hosts (Render, Railway)
  can take 10-30s on the first request after idle — consider mentioning this
  in your project writeup, or converting to TFLite for faster loads.

## Deploy with Docker

```
docker build -t pneumonia-api .
docker run -p 8000:8000 pneumonia-api
```

"""
Pneumonia Detection API
-----------------------
Serves a trained ResNet50-based Keras model (rescale=1./255, target_size=(224,224))
behind a REST endpoint for a React frontend.
"""

import io
import logging

import numpy as np
import tensorflow as tf
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image, UnidentifiedImageError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pneumonia-api")

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MODEL_PATH = "C:\\Users\\vamsi\\OneDrive\\Desktop\\gettnig serious\\DeepLearning\\projects\\pneumonia_detection\\chest_xray_model.h5"   # <-- update to your actual model file
TARGET_SIZE = (224, 224)
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/jpg"}
MAX_FILE_SIZE_MB = 10

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------
app = FastAPI(title="Pneumonia Detection API")

# For local dev this is fine. For deployment, replace "*" with your actual
# frontend URL (e.g. https://your-app.vercel.app) so random sites can't call your API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = None


@app.on_event("startup")
def load_model():
    global model
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        logger.info("Model loaded successfully from %s", MODEL_PATH)
    except Exception as e:
        logger.error("Failed to load model: %s", e)
        # Don't crash the whole app on startup — /health will report it,
        # and /predict will return a clear 503 instead of a confusing 500.
        model = None


# ---------------------------------------------------------------------------
# Preprocessing — must match training exactly
# ---------------------------------------------------------------------------
def preprocess_image(file_bytes: bytes) -> np.ndarray:
    try:
        img = Image.open(io.BytesIO(file_bytes))
        img.verify()  # checks the file isn't truncated/corrupt
        img = Image.open(io.BytesIO(file_bytes))  # reopen after verify()
    except (UnidentifiedImageError, OSError):
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid image.")

    img = img.convert("RGB").resize(TARGET_SIZE)
    arr = np.array(img, dtype=np.float32) / 255.0  # matches your training rescale=1./255
    arr = np.expand_dims(arr, axis=0)
    return arr


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded. Check server logs.")

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{file.content_type}'. Upload a JPEG or PNG.",
        )

    file_bytes = await file.read()
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(status_code=400, detail=f"File too large ({size_mb:.1f}MB). Max {MAX_FILE_SIZE_MB}MB.")

    x = preprocess_image(file_bytes)

    try:
        raw_pred = model.predict(x, verbose=0)[0][0]
    except Exception as e:
        logger.error("Inference failed: %s", e)
        raise HTTPException(status_code=500, detail="Model inference failed.")

    # Assumes sigmoid output where >0.5 = Pneumonia. Flip this if your
    # class indices were the other way around during training.
    is_pneumonia = raw_pred > 0.5
    confidence = float(raw_pred if is_pneumonia else 1 - raw_pred)

    return {
        "label": "Pneumonia" if is_pneumonia else "Normal",
        "confidence": round(confidence * 100, 2),
        "raw_score": round(float(raw_pred), 4),
    }
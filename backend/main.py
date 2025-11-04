# backend/main.py

import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import requests
import joblib

# -------------------- File Paths --------------------
MODEL_PATH = "backend/depression_model.pkl"
VECTORIZER_PATH = "backend/vectorizer.pkl"

# Google Drive direct download links
MODEL_URL = "https://drive.google.com/uc?export=download&id=15Mk4f_NpCkV_zw6A0DSdDLalKPpFNGsX"
VECTORIZER_URL = "https://drive.google.com/uc?export=download&id=1ffHyi06h7KgpwvvahhORaVyX_FGtWtgL"

# Ensure backend folder exists
os.makedirs("backend", exist_ok=True)


# -------------------- Helper: Download files if missing --------------------
def download_file(url: str, dest: str):
    if not os.path.exists(dest):
        print(f"Downloading {os.path.basename(dest)}...")
        response = requests.get(url)
        response.raise_for_status()
        with open(dest, "wb") as f:
            f.write(response.content)
        print(f"{os.path.basename(dest)} downloaded successfully.")


# Download model and vectorizer if not found
download_file(MODEL_URL, MODEL_PATH)
download_file(VECTORIZER_URL, VECTORIZER_PATH)

# -------------------- Load Model and Vectorizer --------------------
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# -------------------- FastAPI Setup --------------------
app = FastAPI(title="MindGuard Depression Detection API", version="1.0")

# Enable CORS for frontend communication (Next.js)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to ["http://localhost:3000"] if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------- Input Schema --------------------
class TextInput(BaseModel):
    text: str


# -------------------- Root Endpoint --------------------
@app.get("/")
def home():
    return {"message": "Welcome to the MindGuard Depression Detection API 🧠"}


# -------------------- Prediction Endpoint --------------------
@app.post("/predict")
def predict(input_data: TextInput):
    vect_text = vectorizer.transform([input_data.text])
    prediction = model.predict(vect_text)[0]
    proba = model.predict_proba(vect_text)[0][1]

    return {
        "input": input_data.text,
        "prediction": int(prediction),
        "probability": float(proba),
        "label": "Depressed" if prediction == 1 else "Not Depressed"
    }

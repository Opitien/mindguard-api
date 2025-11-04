import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
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


# -------------------- Helper: Download files from Google Drive safely --------------------
def download_file_from_google_drive(url: str, destination: str):
    """Stream-download large files from Google Drive safely."""
    if os.path.exists(destination):
        return  # Skip if already downloaded

    print(f"Downloading {os.path.basename(destination)} from Google Drive...")
    session = requests.Session()
    response = session.get(url, stream=True)
    token = None

    # Handle confirmation token (for large files)
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            token = value
            break

    if token:
        params = {"confirm": token}
        response = session.get(url, params=params, stream=True)

    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

    print(f"{os.path.basename(destination)} downloaded successfully.")


# -------------------- Download model/vectorizer if missing --------------------
download_file_from_google_drive(MODEL_URL, MODEL_PATH)
download_file_from_google_drive(VECTORIZER_URL, VECTORIZER_PATH)


# -------------------- Load Model and Vectorizer --------------------
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


# -------------------- FastAPI Setup --------------------
app = FastAPI(title="MindGuard Depression Detection API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific frontend domain if needed
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

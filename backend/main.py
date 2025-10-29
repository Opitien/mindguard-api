# backend/main.py
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# ------------- Load Model and Vectorizer -------------
model = joblib.load("depression_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# ------------- FastAPI Setup -------------
app = FastAPI(title="Depression Detection API", version="1.0")

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------- Input Schema -------------
class TextInput(BaseModel):
    text: str

# ------------- Root Endpoint -------------
@app.get("/")
def home():
    return {"message": "Welcome to the Depression Detection API 🧠"}

# ------------- Prediction Endpoint -------------
@app.post("/predict")
def predict(input_data: TextInput):
    # Vectorize input
    vect_text = vectorizer.transform([input_data.text])

    # Predict label (0 = Not Depressed, 1 = Depressed)
    prediction = model.predict(vect_text)[0]

    # Optional: get probability
    proba = model.predict_proba(vect_text)[0][1]  # probability of depression

    return {
        "input": input_data.text,
        "prediction": int(prediction),
        "probability": float(proba),
        "label": "Depressed" if prediction == 1 else "Not Depressed"
    }

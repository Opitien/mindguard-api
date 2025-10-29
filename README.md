🧠 **MindGuard API**

**MindGuard API** is a machine learning–powered backend built with **FastAPI** that detects signs of depression from user text input.
It’s designed to integrate seamlessly with a **Next.js frontend chatbot UI**, providing instant emotional wellness insights through text analysis.

---

## 🚀 Features

* 🧩 **Machine Learning Model** — trained with a Random Forest classifier to detect depressive language patterns
* ⚡ **FastAPI Backend** — lightweight and high-performance REST API
* 💬 **Integration Ready** — works easily with React or Next.js frontends
* 🧠 **Real-Time Predictions** — returns depression probability and sentiment label
* 🧰 **Deployed on Render (backend)** + **Vercel (frontend)**

---

## 🏗️ Tech Stack

* **Python 3.11+**
* **FastAPI**
* **Scikit-learn**
* **Joblib**
* **Pandas**
* **Uvicorn**

---

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/mindguard-api.git
cd mindguard-api/backend

# Create and activate a virtual environment
python -m venv .venv
source .venv/Scripts/activate  # On Windows
# or
source .venv/bin/activate      # On Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

---

## 🧠 Run the API locally

```bash
uvicorn main:app --reload
```

The server will start at
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🔍 Endpoints

### **GET /**

Returns a welcome message.

```json
{
  "message": "Welcome to the Depression Detection API 🧠"
}
```

---

### **POST /predict**

Analyzes the input text and returns prediction results.

#### Request body:

```json
{
  "text": "I feel tired and unmotivated most of the time."
}
```

#### Response:

```json
{
  "input": "I feel tired and unmotivated most of the time.",
  "prediction": 1,
  "probability": 0.86,
  "label": "Depressed"
}
```

---

## 🌐 Deployment

### **Render (Backend)**

1. Push this repo to GitHub.
2. Go to [Render.com](https://render.com).
3. Click **“New Web Service”** → connect GitHub → select `mindguard-api`.
4. Set the start command to:

   ```
   uvicorn main:app --host 0.0.0.0 --port 10000
   ```
5. Deploy 🎉

### **Vercel (Frontend)**

1. Deploy your Next.js chatbot to [Vercel.com](https://vercel.com).
2. Set the API endpoint to your Render URL:

   ```
   https://mindguard-api.onrender.com/predict
   ```

---

## 🧩 Folder Structure

```
mindguard-api/
│
├── backend/
│   ├── main.py                 # FastAPI entry point
│   ├── depression_model.pkl    # Trained model file
│   ├── vectorizer.pkl          # Text vectorizer
│   ├── requirements.txt
│   └── .venv/
│
└── frontend/
    └── Next.js chatbot UI
```

---

## ✨ Future Enhancements

* Add multilingual support
* Expand emotion categories (anxiety, stress, etc.)
* Integrate real-time mood tracking dashboard

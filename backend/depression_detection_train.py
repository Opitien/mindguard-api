# depression_detection_train.py
# Train a Random Forest model using Hugging Face depression dataset
import joblib
from datasets import load_dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score, classification_report
import pandas as pd

# 1. Load dataset from Hugging Face
print("Loading dataset...")
dataset = load_dataset("thePixel42/depression-detection")
df = pd.DataFrame(dataset["train"])  # use the train split

print("\nDataset preview:")
print(df.head())

# 2. Define features and labels
X = df["text"]
y = df["label"]

# 3. Convert text to numerical features
print("\nVectorizing text...")
vectorizer = TfidfVectorizer(max_features=5000, stop_words="english")
X_vect = vectorizer.fit_transform(X)

# 4. Split into train/test
X_train, X_test, y_train, y_test = train_test_split(X_vect, y, test_size=0.2, random_state=42)

# 5. Create and train Random Forest
print("\nTraining model...")
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# 6. Evaluate performance
print("\nEvaluating model...")
y_pred = model.predict(X_test)


# Save model and vectorizer
joblib.dump(model, "depression_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("\n✅ Model and vectorizer saved successfully!")

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))



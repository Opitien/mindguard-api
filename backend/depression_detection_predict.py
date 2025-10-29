import joblib

# Load the saved model and vectorizer
model = joblib.load("depression_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def predict_depression(text):
    """Predict if a given text indicates depression."""
    # Transform input text
    text_vector = vectorizer.transform([text])
    
    # Make prediction
    prediction = model.predict(text_vector)[0]
    
    # Interpret result
    if prediction == 1:
        return "⚠️ Signs of depression detected."
    else:
        return "✅ No signs of depression detected."

# Example usage
if __name__ == "__main__":
    user_text = input("Enter a message or journal entry: ")
    result = predict_depression(user_text)
    print(result)

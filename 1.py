# Load and inspect your model manually in a Python script or Jupyter Notebook
import joblib

model = joblib.load("phishing_model_sgd.pkl")
print("Classes:", model.classes_)
print("Model type:", type(model))

# Test manually
test_sample = ["Congratulations! You've won a prize. Click here to claim."]
from joblib import load
vectorizer = load('vectorizer.pkl')

X = vectorizer.transform(test_sample)
print("Prediction:", model.predict(X))  # Should ideally return 1 for phishing

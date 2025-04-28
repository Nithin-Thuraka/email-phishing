import logging
import joblib
import re
import numpy as np

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import quote_plus

# Flask setup
app = Flask(__name__)
app.secret_key = 'yoGOCSPX-R0SNaqcIL2ArYeuLDcMoSdF8DePL'
logging.basicConfig(level=logging.INFO)
CORS(app, origins=["http://localhost:3000"], supports_credentials=True)

# MongoDB Atlas setup
username = quote_plus("kushalkumarchv03")
password = quote_plus("Chvkkr03")
uri = f"mongodb+srv://{username}:{password}@cluster0.vvvd13y.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

try:
    client = MongoClient(uri)
    db = client["auth_db"]
    users_collection = db["users"]
    logging.info("✅ MongoDB connected successfully.")
except Exception as e:
    logging.error(f"❌ MongoDB connection failed: {str(e)}")

# Load model and vectorizer
try:
    model = joblib.load('phishing_model_sgd.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    logging.info("✅ Model and vectorizer loaded.")
    logging.info(f"Model classes: {model.classes_}")
except Exception as e:
    logging.error(f"❌ Error loading model/vectorizer: {str(e)}")
    model, vectorizer = None, None

# Clean email content
def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^\w\s@.]", "", text)  # Remove special chars
    return text.lower()

@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({"success": False, "message": "Email and password are required"}), 400

        if users_collection.find_one({"email": email}):
            return jsonify({"success": False, "message": "Email already exists"}), 400

        hashed_password = generate_password_hash(password)
        users_collection.insert_one({"email": email, "password": hashed_password})
        return jsonify({"success": True, "message": "User registered successfully"})
    except Exception as e:
        logging.error(f"/signup error: {str(e)}")
        return jsonify({"success": False, "message": "Server error"}), 500

@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        user = users_collection.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            session["user"] = email
            return jsonify({"success": True, "message": "Login successful"})

        return jsonify({"success": False, "message": "Invalid credentials"}), 401
    except Exception as e:
        logging.error(f"/login error: {str(e)}")
        return jsonify({"success": False, "message": "Server error"}), 500

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        email_text = data.get("email_text", "").strip()

        if not model or not vectorizer:
            return jsonify({"prediction": "Model not loaded"}), 500

        if not email_text:
            return jsonify({"prediction": "Empty text provided"}), 400

        # Clean and transform the email text
        cleaned = clean_text(email_text)
        transformed = vectorizer.transform([cleaned])

        # Get the raw prediction
        prediction_raw = model.predict(transformed)[0]

        # Log the raw prediction and its type for debugging
        logging.info(f"Raw prediction: {prediction_raw} (type: {type(prediction_raw)})")

        # Check the raw prediction value and map it to the final label
        if isinstance(prediction_raw, str):
            logging.info("Raw prediction is already a string: " + prediction_raw)
            prediction_label = prediction_raw  # Directly use the string label ("Phishing Email" or "Safe Email")
        else:
            # For numeric predictions, map them to the final label
            prediction_label = "Phishing Email" if prediction_raw == 1 else "Safe Email"

        # Log the final prediction
        logging.info(f"Final prediction: {prediction_label}")

        return jsonify({"prediction": prediction_label})

    except Exception as e:
        logging.error(f"/predict error: {str(e)}")
        return jsonify({"prediction": "Prediction error"}), 500



@app.route("/test_model", methods=["GET"])
def test_model():
    try:
        test_text = "Congratulations, you've won a prize! Click the link to claim now."
        cleaned = clean_text(test_text)
        transformed = vectorizer.transform([cleaned])
        prediction_raw = model.predict(transformed)[0]
        prediction_label = "Phishing Email" if str(prediction_raw) == '1' else "Safe Email"
        return jsonify({"sample_input": test_text, "prediction": prediction_label})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

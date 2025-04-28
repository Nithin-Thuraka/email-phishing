Email Phishing Detection
This project is designed to detect phishing emails using machine learning techniques. It analyzes email content and predicts whether the email is safe or phishing based on patterns and features extracted from the email body. The model has been trained using a dataset of labeled phishing and legitimate emails.

Features
Real-Time Email Classification: Classifies incoming emails as "safe" or "phishing."

Machine Learning Models: The project uses various machine learning algorithms like Naive Bayes, Random Forest, Decision Trees, and XGBoost to detect phishing emails.

Frontend Interface: A simple React frontend allows users to input email content and receive predictions.

Backend Server: Flask-based backend for handling email content prediction requests using a trained machine learning model.

Tech Stack
Frontend: React.js

Backend: Flask

Machine Learning: Python (scikit-learn, XGBoost, Random Forest, Naive Bayes)

Database: MongoDB (for storing user login details and email data)

Other Libraries: pandas, numpy, matplotlib, seaborn, scikit-learn, TensorFlow (for advanced models like LSTM)

Installation
Prerequisites
Python 3.x: Ensure you have Python installed. You can download it from here.

Node.js: Required for running the frontend. Download from here.

Setup
Clone the repository:

bash
Copy
Edit
git clone https://github.com/Nithin-Thuraka/email-phishing-detection.git
cd email-phishing-detection
Backend Setup (Python):

Create a virtual environment:

bash
Copy
Edit
python -m venv .venv
Activate the virtual environment:

On Windows:

bash
Copy
Edit
.\.venv\Scripts\activate
On macOS/Linux:

bash
Copy
Edit
source .venv/bin/activate
Install the required Python packages:

bash
Copy
Edit
pip install -r requirements.txt
Frontend Setup (React):

Go to the frontend directory:

bash
Copy
Edit
cd frontend
Install the required Node packages:

bash
Copy
Edit
npm install
Run the Backend Server:

bash
Copy
Edit
flask run
This will start the Flask server, typically on http://127.0.0.1:5000.

Run the Frontend:

In the frontend directory, run:

bash
Copy
Edit
npm start
This will start the React frontend on http://localhost:3000.

Usage
Input Email: Enter the body of the email into the input field on the frontend.

Classify: Click the "Predict" button to classify the email as phishing or safe.

View Results: The prediction result will be displayed as either "Safe" or "Phishing."

Model Training
The model is trained using a Kaggle dataset of 17,000 labeled emails. Multiple machine learning algorithms were used, including:

Naive Bayes

Random Forest

XGBoost

Logistic Regression

Support Vector Machines (SVM)

Deep Learning Models (LSTM)

You can retrain the model by running the Python script train_model.py.

Contributing
Feel free to fork the repository and submit pull requests. Contributions are always welcome!

License
This project is licensed under the MIT License - see the LICENSE file for details.

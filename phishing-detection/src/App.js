import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Ensure the CSS is correctly linked

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [authMode, setAuthMode] = useState('login');
  const [form, setForm] = useState({ email: '', password: '' });
  const [emailText, setEmailText] = useState('');
  const [prediction, setPrediction] = useState('');
  const [authError, setAuthError] = useState('');
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleAuth = async () => {
    if (!form.email || !form.password) {
      setAuthError('Please enter email and password');
      return;
    }

    setLoading(true);
    try {
      const endpoint = authMode === 'signup' ? '/signup' : '/login';
      const res = await axios.post(`http://127.0.0.1:5000${endpoint}`, form, { withCredentials: true });
      if (res.data.success) {
        setIsAuthenticated(true);
        setAuthError('');
      } else {
        setAuthError(res.data.message);
      }
    } catch (err) {
      console.error(err);
      setAuthError('Incorrect Credentials');
    } finally {
      setLoading(false);
    }
  };

  const handlePredict = async () => {
    if (!emailText.trim()) {
      setErrorMessage('Please input the email to predict');
      setPrediction(''); // Clear previous prediction if no input
      return;
    }

    setLoading(true);
    setErrorMessage('');
    setPrediction(''); // Clear previous prediction before making request

    try {
      const res = await axios.post('http://127.0.0.1:5000/predict', { email_text: emailText });
      console.log("Received prediction:", res.data.prediction);
      setPrediction(res.data.prediction);
    } catch (err) {
      console.error(err);
      setPrediction('Error predicting');
    } finally {
      setLoading(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="auth-wrapper">
        <div className="auth-box">
          <h2>{authMode === 'signup' ? 'Sign Up' : 'Log In'}</h2>
          <input name="email" type="email" value={form.email} onChange={handleChange} placeholder="Email" />
          <input name="password" type="password" value={form.password} onChange={handleChange} placeholder="Password" />
          <button onClick={handleAuth} disabled={loading}>
            {loading ? 'Loading...' : authMode === 'signup' ? 'Sign Up' : 'Log In'}
          </button>
          <p>
            {authMode === 'signup' ? 'Already have an account?' : 'New user?'}{' '}
            <span onClick={() => setAuthMode(authMode === 'signup' ? 'login' : 'signup')} style={{ color: 'blue', cursor: 'pointer' }}>
              {authMode === 'signup' ? 'Log in' : 'Sign up'}
            </span>
          </p>
          {authError && <div className="error-msg">{authError}</div>}
        </div>
      </div>
    );
  }

  return (
    <div className="main-container">
      <h1>Email Phishing Detector</h1>

      <textarea
        value={emailText}
        onChange={(e) => setEmailText(e.target.value)}
        placeholder="Paste email here..."
        rows={8}
        cols={50}
      />

      <button onClick={handlePredict} disabled={loading}>
        {loading ? 'Checking...' : 'Check Email'}
      </button>

      {errorMessage && <div className="error-msg">{errorMessage}</div>} {/* Display error if input is empty */}

      {prediction && (
        <div className="prediction-result">
          <h3>Prediction Result:</h3>
          <span className={prediction.trim() === 'Phishing Email' ? 'prediction red' : 'prediction green'}>
            {prediction}
          </span>
        </div>
      )}
    </div>
  );
}

export default App;

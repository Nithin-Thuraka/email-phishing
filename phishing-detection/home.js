import React, { useState } from 'react';
import AuthPage from './AuthPage';
import App from './App';

function Home() {
  const [authenticated, setAuthenticated] = useState(false);

  return authenticated ? <App /> : <AuthPage onAuthSuccess={() => setAuthenticated(true)} />;
}

export default Home;

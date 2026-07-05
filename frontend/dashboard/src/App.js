import React, { useState } from 'react';
import Login from './Login';
import Chat from './Chat';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  if (!token) {
    return <Login onLoginSuccess={setToken} />;
  }

  return <Chat token={token} onLogout={handleLogout} />;
}

export default App;
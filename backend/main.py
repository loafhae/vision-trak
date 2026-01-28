import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [view, setView] = useState('login'); // login, dashboard
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  
  // Login Logic
  const handleLogin = async () => {
    try {
      const res = await axios.post('http://localhost:8000/login', { username, password });
      if (res.data.role === 'Super Admin' || res.data.role === 'Barangay Official') {
        setView('dashboard');
      } else {
        alert("Access Denied: Residents must use the Mobile App.");
      }
    } catch (err) {
      alert("Login Failed");
    }
  };

  return (
    <div className="App">
      {view === 'login' ? (
        <div className="login-box">
          <h2>Admin Portal</h2>
          <input placeholder="Username" onChange={e => setUsername(e.target.value)} />
          <input type="password" placeholder="Password" onChange={e => setPassword(e.target.value)} />
          <button onClick={handleLogin}>Login</button>
        </div>
      ) : (
        <Dashboard />
      )}
    </div>
  );
}

// --- DASHBOARD COMPONENT ---
function Dashboard() {
  const [newUser, setNewUser] = useState({ username: '', password: '', role: 'Resident' });

  // FR1: Add User Logic with CONFIRMATION MODAL
  const handleAddUser = async () => {
    // STRICT REQUIREMENT: Confirmation Modal (Fig 3.7.7)
    if (window.confirm("Are you sure you want to ADD this user?")) {
      await axios.post('http://localhost:8000/users', newUser);
      alert("User Added!");
    }
  };

  return (
    <div className="dashboard">
      <h1>Barangay Admin Dashboard</h1>
      
      <div className="card">
        <h3>Create New Account</h3>
        <input placeholder="Username" onChange={e => setNewUser({...newUser, username: e.target.value})} />
        <input placeholder="Password" onChange={e => setNewUser({...newUser, password: e.target.value})} />
        <select onChange={e => setNewUser({...newUser, role: e.target.value})}>
          <option value="Resident">Resident</option>
          <option value="Barangay Official">Barangay Official</option>
        </select>
        <button onClick={handleAddUser}>Create Account</button>
      </div>
    </div>
  );
}

export default App;
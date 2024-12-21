import React, { useState } from "react";
import axios from "axios";

function Login({ setToken }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    // Input Validation
    if (!username.trim() || !password.trim()) {
      setError("Both username and password are required.");
      return;
    }

    try {
      const response = await axios.post("http://127.0.0.1:8000/auth/login", {
        username: username.trim(),
        password: password.trim(),
      });
      localStorage.setItem("token", response.data.access_token);
      localStorage.setItem("user_id", response.data.user_id); // Store user_id
      setToken(response.data.access_token);
      alert("Login Successful!");
    } catch (error) {
      setError("Login failed. Please check your credentials.");
      console.error(error.response?.data || error.message);
    }
  };

  return (
    <form onSubmit={handleLogin} className="max-w-md mx-auto p-6 shadow-md rounded bg-white">
      <h2 className="text-2xl font-bold mb-4">Login</h2>
      {error && <p className="text-red-500 mb-2">{error}</p>}
      <div className="mb-4">
        <label className="block text-gray-700 mb-2">Username</label>
        <input
          type="text"
          className="w-full p-2 border rounded"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>
      <div className="mb-4">
        <label className="block text-gray-700 mb-2">Password</label>
        <input
          type="password"
          className="w-full p-2 border rounded"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>
      <button className="w-full p-2 bg-blue-500 text-white rounded">Login</button>
    </form>
  );
}
export default Login;

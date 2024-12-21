import React, { useState } from "react";
import axios from "axios";

function Register() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();
    console.log("Register function triggered"); // Debugging
    // Validation
    if (!username.trim() || !password.trim()) {
      setError("Both username and password are required.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters long.");
      return;
    }
    try {
      const response = await axios.post("http://127.0.0.1:8000/auth/register", {
        username: username.trim(),
        password: password.trim(),
      });
      console.log("Response:", response.data); // Debugging
      alert("Registration Successful!");
    } catch (error) {
      console.error("Registration Error:", error.response?.data || error.message);
      alert("Registration Failed!");
    }
  };

  return (
    <form onSubmit={handleRegister}>
      <h2>Register</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button type="submit">Register</button>
    </form>
  );
}

export default Register;

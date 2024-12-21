import React, { useState } from "react";
import "../styles/LoginPage.css";

const LoginPage = () => {
    const [formData, setFormData] = useState({ email: "", password: "" });
    const [error, setError] = useState("");

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({ ...formData, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!formData.email || !formData.password) {
            setError("Both fields are required!");
            return;
        }
        if (!/\S+@\S+\.\S+/.test(formData.email)) {
            setError("Invalid email format!");
            return;
        }
        setError("");
        // Simulate login API call
        console.log("Logging in with:", formData);
        alert("Login successful!");
    };

    return (
        <div className="login-container">
            <div className="login-card">
                <h2>Log In</h2>
                {error && <p className="error-message">{error}</p>}
                <form onSubmit={handleSubmit} className="login-form">
                    <input
                        type="email"
                        name="email"
                        placeholder="Email"
                        value={formData.email}
                        onChange={handleChange}
                        required
                    />
                    <input
                        type="password"
                        name="password"
                        placeholder="Password"
                        value={formData.password}
                        onChange={handleChange}
                        required
                    />
                    <button type="submit" className="login-button">
                        Log In
                    </button>
                </form>
                <p className="forgot-password">
                    <a href="/forgot-password">Forgot Password?</a>
                </p>
                <p className="register-redirect">
                    Don't have an account? <a href="/register">Sign up</a>
                </p>
            </div>
        </div>
    );
};

export default LoginPage;

import React from "react";
import "../styles/LandingPage.css";

const LandingPage = () => {
    return (
        <div className="landing-container">
            <div className="signup-card">
                <h2>Sign Up</h2>
                <div className="social-login">
                    <button className="google-button">G</button>
                    <span>|</span>
                    <button className="github-button">GH</button>
                </div>
                <div className="divider">
                    <span>Or</span>
                </div>
                <form className="signup-form">
                    <div className="name-fields">
                        <input type="text" placeholder="First Name" required />
                        <input type="text" placeholder="Last Name" required />
                    </div>
                    <input type="email" placeholder="Email" required />
                    <input type="tel" placeholder="Phone Number" required />
                    <input
                        type="password"
                        placeholder="Password"
                        required
                        pattern="(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*\W).{8,}"
                        title="Minimum 8 chars, 1 uppercase, 1 number, and 1 special character"
                    />
                    <p className="password-note">
                        Minimum 8 chars, 1 uppercase, 1 number, and 1 special char.
                    </p>
                    <button type="submit" className="get-started-button">
                        Get started
                    </button>
                </form>
                <p className="login-redirect">
                    Already have an account? <a href="/login">Log in</a>
                </p>
            </div>
        </div>
    );
};

export default LandingPage;

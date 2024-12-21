import React from "react";
import "./Dashboard.css";

const Dashboard = () => {
    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <h1>Welcome to NERO!</h1>
                <p>Your personal assistant for productivity and organization.</p>
            </header>
            <div className="dashboard-navigation">
                <button className="dashboard-button">Task Management</button>
                <button className="dashboard-button">Schedule Management</button>
                <button className="dashboard-button">AI Interaction</button>
                <button className="dashboard-button">Settings</button>
            </div>
        </div>
    );
};

export default Dashboard;

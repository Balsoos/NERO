import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Auth/Login";
import Register from "./components/Auth/Register";
import TasksPage from "./pages/TasksPage";
import SchedulesPage from "./pages/SchedulesPage";
import EventPage from "./pages/EventPage";
import ChatPage from "./pages/ChatPage";

function App() {
  const [token, setToken] = useState(localStorage.getItem("token") || null);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setToken(null);
  };

  return (
    <Router>
      <div>
        <header>
          <nav>
            <a href="/">Home</a>
            {!token ? (
              <>
                <a href="/login">Login</a>
                <a href="/register">Register</a>
              </>
            ) : (
              <>
                <a href="/chat">Chat</a>
                <a href="/tasks">Tasks</a>
                <a href="/schedule">Schedule</a>
                <a href="/events">Create Event</a>
                <button onClick={handleLogout}>Logout</button>
              </>
            )}
          </nav>
        </header>

        <main>
          <Routes>
            <Route path="/" element={<h1>Welcome to NERO AI Personal Assistant</h1>} />
            <Route
              path="/login"
              element={!token ? <Login setToken={(t) => { localStorage.setItem("token", t); setToken(t); }} /> : <Navigate to="/" />}
            />
            <Route
              path="/register"
              element={!token ? <Register /> : <Navigate to="/" />}
            />
            <Route
              path="/chat"
              element={token ? <ChatPage token={token} /> : <Navigate to="/login" />}
            />
            <Route
              path="/tasks"
              element={token ? <TasksPage token={token} /> : <Navigate to="/login" />}
            />
            <Route
              path="/schedule"
              element={token ? <SchedulesPage token={token} /> : <Navigate to="/login" />}
            />
            <Route
              path="/events"
              element={token ? <EventPage token={token} /> : <Navigate to="/login" />}
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;

import React, { useState } from "react";
import axios from "axios";

function ChatBox({ token }) {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");

    const sendMessage = async () => {
        if (!input.trim()) {
            alert("Message cannot be empty!");
            return;
        }

        const userId = localStorage.getItem("user_id");
        if (!userId) {
            alert("User ID is not available. Please log in again.");
            return;
        }

        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/chat/chat",
                {
                    user_id: parseInt(userId), // Ensure user_id is an integer
                    message: input.trim(),
                },
                {
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );

            setMessages([...messages, { user: input, ai: response.data.ai_reply }]);
            setInput(""); // Clear the input
        } catch (error) {
            console.error("Chat Error:", error.response?.data || error.message);
            alert("Failed to send message: " + (error.response?.data?.detail || error.message));
        }
    };

    return (
        <div>
            <h2>Chat with NERO</h2>
            <div>
                {messages.map((msg, index) => (
                    <div key={index}>
                        <p><strong>You:</strong> {msg.user}</p>
                        <p><strong>NERO:</strong> {msg.ai}</p>
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Type your message..."
            />
            <button onClick={sendMessage}>Send</button>
        </div>
    );
}

export default ChatBox;

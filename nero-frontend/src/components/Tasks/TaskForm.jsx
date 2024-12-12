import React, { useState } from "react";
import api from "../../services/api";

const TaskForm = ({ onTaskAdded }) => {
    const [description, setDescription] = useState("");
    const [priority, setPriority] = useState("medium");

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            await api.post("/tasks", { description, priority });
            alert("Task added successfully!");
            onTaskAdded();
            setDescription("");
        } catch (err) {
            console.error("Failed to add task:", err);
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                placeholder="Task Description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
            />
            <select value={priority} onChange={(e) => setPriority(e.target.value)}>
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
            </select>
            <button type="submit">Add Task</button>
        </form>
    );
};

export default TaskForm;

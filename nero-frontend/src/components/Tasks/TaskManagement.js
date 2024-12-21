import React, { useState, useEffect } from "react";
import axios from "axios";

function TaskManagement({ token }) {
    const [tasks, setTasks] = useState([]);
    const [newTask, setNewTask] = useState({ description: "", priority: "medium", due_date: "" });

    useEffect(() => {
        async function fetchTasks() {
            try {
                const response = await axios.get("http://127.0.0.1:8000/tasks", {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setTasks(response.data);
            } catch (error) {
                console.error("Error fetching tasks:", error.response?.data || error.message);
                alert("Failed to fetch tasks.");
            }
        }
        fetchTasks();
    }, [token]);

    const handleCreateTask = async () => {
        try {
            const response = await axios.post("http://127.0.0.1:8000/tasks", newTask, {
                headers: { Authorization: `Bearer ${token}` },
            });
            alert("Task created successfully!");
            setTasks([...tasks, response.data]);
            setNewTask({ description: "", priority: "medium", due_date: "" });
        } catch (error) {
            console.error("Error creating task:", error.response?.data || error.message);
            alert("Failed to create task.");
        }
    };

    const handleDeleteTask = async (taskId) => {
        try {
            await axios.delete(`http://127.0.0.1:8000/tasks/${taskId}`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            alert("Task deleted successfully!");
            setTasks(tasks.filter(task => task.id !== taskId));
        } catch (error) {
            console.error("Error deleting task:", error.response?.data || error.message);
            alert("Failed to delete task.");
        }
    };

    return (
        <div>
            <h2>Task Management</h2>
            <div>
                <h3>Create New Task</h3>
                <input
                    type="text"
                    placeholder="Description"
                    value={newTask.description}
                    onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                />
                <input
                    type="text"
                    placeholder="Priority"
                    value={newTask.priority}
                    onChange={(e) => setNewTask({ ...newTask, priority: e.target.value })}
                />
                <input
                    type="datetime-local"
                    value={newTask.due_date}
                    onChange={(e) => setNewTask({ ...newTask, due_date: e.target.value })}
                />
                <button onClick={handleCreateTask}>Create Task</button>
            </div>
            <div>
                <h3>Tasks</h3>
                <ul>
                    {tasks.map(task => (
                        <li key={task.id}>
                            <p>{task.description} (Priority: {task.priority})</p>
                            <button onClick={() => handleDeleteTask(task.id)}>Delete</button>
                        </li>
                    ))}
                </ul>
            </div>
        </div>
    );
}

export default TaskManagement;

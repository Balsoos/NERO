import React from "react";

function TaskCard({ task }) {
    return (
        <div style={{ border: "1px solid #ccc", padding: "10px", margin: "10px 0" }}>
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <p><strong>Status:</strong> {task.status}</p>
            {task.due_date && <p><strong>Due:</strong> {new Date(task.due_date).toLocaleString()}</p>}
        </div>
    );
}

export default TaskCard;

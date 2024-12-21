import React from "react";
import TaskManagement from "../components/Tasks/TaskManagement";

function TasksPage({ token }) {
    return (
        <div>
            <h1>Tasks</h1>
            <TaskManagement token={token} />
        </div>
    );
}

export default TasksPage;

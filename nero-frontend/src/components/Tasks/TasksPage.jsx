import React, { useState } from "react";
import TaskForm from "./TaskForm";
import TaskList from "./TaskList";

const TasksPage = () => {
    const [refresh, setRefresh] = useState(false);

    const handleTaskAdded = () => {
        setRefresh(!refresh);
    };

    return (
        <div>
            <h1>Task Management</h1>
            <TaskForm onTaskAdded={handleTaskAdded} />
            <TaskList key={refresh} />
        </div>
    );
};

export default TasksPage;

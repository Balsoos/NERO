import React from "react";
import TaskCard from "./TaskCard";

function TaskList({ tasks }) {
    if (!tasks || tasks.length === 0) {
        return <p>No tasks found. Start by creating one!</p>;
    }

    return (
        <div>
            {tasks.map((task) => (
                <TaskCard key={task.id} task={task} />
            ))}
        </div>
    );
}

export default TaskList;

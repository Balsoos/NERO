import { render, screen, fireEvent } from "@testing-library/react";
import TaskManagement from "../components/Tasks/TaskManagement";

test("renders task management component", () => {
    render(<TaskManagement token="test_token" />);
    expect(screen.getByText(/Task Management/i)).toBeInTheDocument();
});

test("handles creating a new task", () => {
    render(<TaskManagement token="test_token" />);

    fireEvent.change(screen.getByPlaceholderText("Description"), { target: { value: "New Task" } });
    fireEvent.change(screen.getByPlaceholderText("Priority"), { target: { value: "High" } });
    fireEvent.click(screen.getByText(/Create Task/i));

    // Ideally, mock the API and check if the task appears in the UI
});

import { render, screen, fireEvent } from "@testing-library/react";
import Login from "../components/Auth/Login";

test("renders login form", () => {
    render(<Login />);
    expect(screen.getByText(/Login/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Username/i)).toBeInTheDocument();
    expect(screen.getByPlaceholderText(/Password/i)).toBeInTheDocument();
});

test("handles login validation errors", () => {
    render(<Login />);
    fireEvent.click(screen.getByText(/Login/i));
    expect(screen.getByText(/Both username and password are required/i)).toBeInTheDocument();
});

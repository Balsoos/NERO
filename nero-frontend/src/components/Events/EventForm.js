import React, { useState } from "react";
import axios from "axios";

function EventForm({ token }) {
    const [summary, setSummary] = useState("");
    const [start, setStart] = useState("");
    const [end, setEnd] = useState("");
    const [error, setError] = useState("");

    const formatDateTime = (datetime) => {
        // Add ":00" for seconds if not present
        if (datetime.length === 16) {
            return `${datetime}:00`;
        }
        return datetime;
    };

    const createEvent = async () => {
        if (!summary.trim() || !start.trim() || !end.trim()) {
            alert("All fields are required to create an event.");
            return;
        }
        if (new Date(start) >= new Date(end)) {
            setError("Start time must be before end time.");
            return;
        }
        try {
            // Format datetime values
            const formattedStart = formatDateTime(start);
            const formattedEnd = formatDateTime(end);

            await axios.post(
                "http://127.0.0.1:8000/events/create-event",
                { summary, start: formattedStart, end: formattedEnd },
                { headers: { Authorization: `Bearer ${token}` } }
            );
            alert("Event Created Successfully!");
        } catch (error) {
            console.error("Event Creation Error:", error.response?.data || error.message);
            alert("Failed to create event: " + (error.response?.data?.detail || error.message));
        }
    };

    return (
        <form
            onSubmit={(e) => {
                e.preventDefault();
                createEvent();
            }}
        >
            <h2>Create Event</h2>
            <input
                type="text"
                placeholder="Event Summary"
                value={summary}
                onChange={(e) => setSummary(e.target.value)}
            />
            <input
                type="datetime-local"
                value={start}
                onChange={(e) => setStart(e.target.value)}
            />
            <input
                type="datetime-local"
                value={end}
                onChange={(e) => setEnd(e.target.value)}
            />
            <button type="submit">Create Event</button>
        </form>
    );
}

export default EventForm;

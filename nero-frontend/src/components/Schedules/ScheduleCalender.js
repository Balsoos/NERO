import React, { useEffect, useState } from "react";
import axios from "axios";

function ScheduleCalendar({ token }) {
    const [events, setEvents] = useState([]);

    useEffect(() => {
        const fetchEvents = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:8000/events", {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setEvents(response.data);
            } catch (error) {
                console.error("Error fetching events:", error);
            }
        };
        fetchEvents();
    }, [token]);

    return (
        <div>
            <h2>Schedule</h2>
            <ul>
                {events.map((event) => (
                    <li key={event.id}>
                        <strong>{event.summary}</strong> <br />
                        From: {new Date(event.start).toLocaleString()} <br />
                        To: {new Date(event.end).toLocaleString()}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ScheduleCalendar;

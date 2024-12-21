import React from "react";
import EventForm from "../components/Events/EventForm";

function EventPage({ token }) {
    return (
        <div>
            <h1>Create an Event</h1>
            <EventForm token={token} />
        </div>
    );
}

export default EventPage;

import ScheduleCard from "./ScheduleCard";

return (
    <div>
        <h2>Schedule</h2>
        {events.map((event) => (
            <ScheduleCard key={event.id} event={event} />
        ))}
    </div>
);

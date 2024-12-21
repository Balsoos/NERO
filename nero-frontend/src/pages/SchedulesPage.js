import React from "react";
import ScheduleCalendar from "../components/Schedules/ScheduleCalender.js";

function SchedulesPage({ token }) {
    return (
        <div>
            <h1>Schedules</h1>
            <ScheduleCalendar token={token} />
        </div>
    );
}

export default SchedulesPage;

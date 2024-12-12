from fastapi import APIRouter
from datetime import datetime, timedelta
from app.services.scheduler import schedule_task_reminder

router = APIRouter()

@router.get("/test-reminder")
def test_reminder():
    task_id = 1
    user_email = "testuser@example.com"
    reminder_time = datetime.utcnow() + timedelta(minutes=2)
    schedule_task_reminder(task_id, user_email, reminder_time)
    return {"message": f"Test reminder scheduled for {reminder_time}"}

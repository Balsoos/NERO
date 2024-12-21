import pytest
from app.services.scheduler import schedule_task_reminder

@pytest.mark.asyncio
async def test_schedule_task_reminder():
    # Mock user email and reminder time
    user_email = "test@example.com"
    task_id = 1
    reminder_time = datetime.utcnow() + timedelta(minutes=10)
    
    schedule_task_reminder(task_id, user_email, reminder_time)
    # Assert scheduler logs or database entries for the scheduled reminder

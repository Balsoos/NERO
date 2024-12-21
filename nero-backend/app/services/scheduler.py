from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
from app.services.email_service import send_email
from app.database import SessionLocal
from app.models.task import Task

jobstores = {
    "default": SQLAlchemyJobStore(url="sqlite:///jobs.db")  # Scheduler jobs stored in a separate DB
}

scheduler = BackgroundScheduler(jobstores=jobstores)
scheduler.start()

def schedule_task_reminder(task_id: int, user_email: str, reminder_time: datetime):
    def send_task_reminder():
        with SessionLocal() as db:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                send_email(user_email, "Task Reminder", f"Reminder for your task: {task.description}")
    
    scheduler.add_job(
        send_task_reminder,
        trigger=DateTrigger(run_date=reminder_time),
        id=f"task_reminder_{task_id}",
        replace_existing=True,
    )
    print(f"Reminder scheduled for task {task_id} at {reminder_time}.")

def remove_task_reminder(task_id: int):
    scheduler.remove_job(job_id=f"task_reminder_{task_id}")
    print(f"Reminder removed for task {task_id}.")

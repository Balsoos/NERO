from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.task import Task

def get_recommendations(db: Session, user_id: int):
    """Generate personalized task recommendations."""
    now = datetime.utcnow()

    # Fetch tasks for the user
    tasks = db.query(Task).filter(Task.user_id == user_id).all()

    # Categorize tasks
    high_priority_tasks = [task for task in tasks if task.priority == "high"]
    due_soon_tasks = [
        task for task in tasks if task.due_date and now <= task.due_date <= now + timedelta(days=2)
    ]
    overdue_tasks = [
        task for task in tasks if task.due_date and task.due_date < now
    ]

    # Combine recommendations
    recommendations = {
        "high_priority": high_priority_tasks,
        "due_soon": due_soon_tasks,
        "overdue": overdue_tasks,
    }

    return recommendations

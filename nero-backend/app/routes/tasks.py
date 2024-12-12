from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.task import Task, TaskResponse
from app.services.auth_service import decode_access_token
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from datetime import datetime, timedelta
from app.services.logger import log_info, log_error
from app.services.scheduler import schedule_task_reminder, remove_task_reminder
from app.models.preferences import preferences
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
@router.get("/test")
def test_openai():
    return {"message": "OpenAI route is working!"}
# Pydantic models
class TaskCreate(BaseModel):
    description: str
    priority: str = "medium"
    due_date: datetime = None

class TaskUpdate(BaseModel):
    description: str = None
    status: str = None
    priority: str = None
    due_date: datetime = None

def get_current_user(token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return username
# Create a new task
@router.post("/", response_model=dict)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    # Get user preference for reminder time
    reminder_time_minutes = user.preferences.reminder_time if user.preferences else 60

    new_task = Task(
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        created_at=datetime.utcnow()
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    # Schedule a reminder based on user preference
    if task.due_date:
        reminder_time = task.due_date - timedelta(minutes=reminder_time_minutes)
        schedule_task_reminder(new_task.id, current_user, reminder_time)

    return {"message": "Task created successfully", "task_id": new_task.id}
# Get all tasks
@router.get("/", response_model=list)
def get_all_tasks(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    tasks = db.query(Task).all()
    return tasks

# Get a task by ID
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Update a task
@router.put("/{task_id}", response_model=dict)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task_update.description:
        task.description = task_update.description
    if task_update.status:
        task.status = task_update.status
    if task_update.priority:
        task.priority = task_update.priority
    if task_update.due_date:
        task.due_date = task_update.due_date

    db.commit()
    db.refresh(task)
    return {"message": "Task updated successfully"}

# Delete a task
@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    db.delete(task)
    db.commit()

    # Remove the scheduled reminder if it exists
    try:
        remove_task_reminder(task_id)
    except Exception:
        pass

    return {"message": "Task deleted successfully."}
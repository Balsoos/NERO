from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, field_validator, ConfigDict
from app.models import Task
from app.auth import get_current_user
from db.database import get_db, Base
from datetime import datetime, timezone
from app.models import Task, User

router = APIRouter()

class TaskCreate(BaseModel):
    description: str
    priority: str = "medium"
    due_date: Optional[datetime] = None

    @field_validator("due_date", mode="before")
    def parse_due_date(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value

class TaskUpdate(BaseModel):
    description: str = None
    status: str = None
    priority: str = None
    due_date: datetime = None    

class TaskResponse(TaskCreate):
    id: int
    id: int
    description: str
    priority: str
    due_date: Optional[datetime]
    status: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
class TaskResponse(BaseModel):
    id: int
    description: str
    priority: str
    due_date: Optional[datetime]
    status: str
    created_at: datetime  # Include the missing field

    class Config:
        from_attributes = True  # Updated for Pydantic v2

@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.user_id == current_user.id).all()
    return tasks

@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    
    new_task = Task(
        description=task.description,
        priority=task.priority,
        due_date=task.due_date,
        created_at=datetime.now(timezone.utc), 
        user_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return TaskResponse(
        id=new_task.id,
        description=new_task.description,
        priority=new_task.priority,
        due_date=new_task.due_date,
        status=new_task.status,
        created_at=new_task.created_at
    )
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


@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")
    
    db.delete(task)
    db.commit()

    return {"message": "Task deleted successfully."}
# app/routes/openai.py

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.openai_service import parse_task_input
from app.models.task import Task
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

@router.get("/test")
def test_openai():
    return {"message": "OpenAI route is working!"}

class NaturalLanguageInput(BaseModel):
    input_text: str

@router.post("/tasks/nlp", response_model=dict)
def create_task_from_nlp(input_data: NaturalLanguageInput, db: Session = Depends(get_db)):
    task_data = parse_task_input(input_data.input_text)
    if not task_data:
        raise HTTPException(status_code=500, detail="Failed to parse task description.")

    # Extract data with defaults
    description = task_data.get('description')
    due_date_str = task_data.get('due_date')
    priority = task_data.get('priority') or 'medium'

    if not description:
        raise HTTPException(status_code=400, detail="Task description is required.")

    # Convert due_date to datetime if provided
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.fromisoformat(due_date_str)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid due date format. Use ISO 8601.")

    new_task = Task(
        description=description,
        priority=priority.lower(),
        due_date=due_date,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created successfully from NLP input", "task_id": new_task.id}

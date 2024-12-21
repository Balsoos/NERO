from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
from pydantic import BaseModel
from datetime import datetime

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    status = Column(String, default="pending")  # pending, completed
    priority = Column(String, default="medium")  # low, medium, high
    due_date = Column(DateTime, nullable=True)
    category = Column(String, nullable=True)  # New category field
    created_at = Column(DateTime, default=datetime.utcnow)
# Pydantic model
class TaskBase(BaseModel):
    title: str
    description: str
    completed: bool

class TaskCreate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int

    class Config:
         from_attributes = True
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskRecommendation(BaseModel):
    id: int
    description: str
    priority: str
    due_date: Optional[datetime]
    status: str

    class Config:
        orm_mode = True

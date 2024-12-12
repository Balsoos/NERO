from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.preferences import Preferences
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/", response_model=dict)
def get_preferences(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if not user.preferences:
        return {"reminder_time": 60}  # Default value
    
    return {"reminder_time": user.preferences.reminder_time}

@router.put("/", response_model=dict)
def update_preferences(reminder_time: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    if reminder_time <= 0:
        raise HTTPException(status_code=400, detail="Reminder time must be a positive number.")
    
    user = db.query(User).filter(User.username == current_user).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    if not user.preferences:
        user.preferences = Preferences(reminder_time=reminder_time)
    else:
        user.preferences.reminder_time = reminder_time
    
    db.commit()
    return {"message": "Preferences updated successfully", "reminder_time": reminder_time}

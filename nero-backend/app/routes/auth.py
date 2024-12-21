from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from Midterm_submission.app import get_password_hash
from app.database import get_db
from app.models.user import User
from app.services.auth_service import hash_password, verify_password, create_access_token
from pydantic import BaseModel
from app.utils.logger import log_info, log_warning
from app.utils.validators import validate_email

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=Dict[str, str])
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    validate_email(user.email)  # Validate email
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered."
        )

    hashed_password = hash_password(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully."}
@router.post("/login", response_model=TokenResponse)
def login_user(user: UserCreate, db: Session = Depends(get_db)):
    log_info(f"Login attempt for user: {user.username}")
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        log_warning(f"Login failed for user: {user.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": db_user.username})
    log_info(f"User {user.username} logged in successfully.")
    return {"access_token": access_token, "token_type": "bearer"}
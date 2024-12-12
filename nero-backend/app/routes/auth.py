from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.services.auth_service import hash_password, verify_password, create_access_token
from pydantic import BaseModel
from app.services.logger import log_info, log_warning

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
@router.post("/register", response_model=dict)
@router.post("/register", response_model=dict)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    log_info(f"Registration attempt for user: {user.username}")
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        log_warning(f"Registration failed: Username {user.username} already exists.")
        raise HTTPException(status_code=400, detail="Username already registered.")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    log_info(f"User {user.username} registered successfully.")
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
import os
from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
print("Starting NERO FastAPI server from:", __file__)

# Load environment variables
load_dotenv()

# Secret key to encode JWTs
SECRET_KEY = "JALdor#65"  # Replace this with a strong key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define the FastAPI app
app = FastAPI()

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load your API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Please check your environment variables.")
client = OpenAI(api_key=api_key)

# Database setup
engine = create_engine('sqlite:///nero.db')
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Task Model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.start()

# User data model
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Database mock-up (for demonstration purposes)
fake_users_db = {
    "johnsmith": {
        "username": "johnsmith",
        "full_name": "John Smith",
        "email": "johnsmith@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
    }
}

# Token data model
class Token(BaseModel):
    access_token: str
    token_type: str

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Get hashed password
def get_password_hash(password):
    return pwd_context.hash(password)

# Get a user from the database
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# Authenticate user
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Create an access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get the current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user

# Dependency to get the current active user
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Route to create token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route to get user profile
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user

# Endpoint to interact with OpenAI API
@app.post("/ask")
async def ask_nero(request: Request):
    body = await request.json()
    user_input = body.get("input")
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": user_input
                }
            ],
            max_tokens=150
        )
        # Corrected way to access the response content
        message_content = response.choices[0].message.content
        return {"response": message_content.strip()}
    except Exception as e:
        print(f"Error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))




# Endpoint to add a task with database support
@app.post("/tasks")
async def add_task(description: str):
    new_task = Task(description=description)
    db.add(new_task)
    db.commit()
    return {"message": "Task added successfully."}

# Scheduler example function
def scheduled_task():
    print(f"Scheduled task executed at {datetime.now()}")

scheduler.add_job(scheduled_task, 'interval', minutes=10)

# Email notification function
def send_email(to_email: str, subject: str, body: str):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_server, smtp_port, smtp_user, smtp_password]):
        raise RuntimeError("SMTP settings are not properly configured.")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())

# Endpoint to send email notification
@app.post("/send-email")
async def email_notification(to_email: str, subject: str, body: str):
    try:
        send_email(to_email, subject, body)
        return {"message": "Email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Public route
@app.get("/")
def read_root():
    return {"message": "Welcome to NERO AI Personal Assistant Backend"}

'''from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timedelta

# Secret key to encode JWTs
SECRET_KEY = "JALdor#65"  # Replace this with a strong key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Define the FastAPI app
app = FastAPI()

# OAuth2 setup
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User data model
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

# Database mock-up (for demonstration purposes)
fake_users_db = {
    "johnsmith": {
        "username": "johnsmith",
        "full_name": "John Smith",
        "email": "johnsmith@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
    }
}

# Token data model
class Token(BaseModel):
    access_token: str
    token_type: str

# Verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Get hashed password
def get_password_hash(password):
    return pwd_context.hash(password)

# Get a user from the database
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# Authenticate user
def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

# Create an access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Dependency to get the current user
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = Token(access_token=token, token_type="bearer")
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username)
    if user is None:
        raise credentials_exception
    return user

# Dependency to get the current active user
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

# Route to create token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Protected route to get user profile
@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
from fastapi import Request

@app.post("/ask")
async def ask(request: Request):
    body = await request.json()
    user_input = body.get("input")
    # Basic response logic (customize as needed)
    response = {"message": f"You asked about '{user_input}'. Here is an answer about vibrant colors."}
    return response

# Public route
@app.get("/")
def read_root():
    return {"message": "Welcome to NERO AI Personal Assistant Backend"}
'''

'''
import os
from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI

# Define your FastAPI app
app = FastAPI()

# Load your API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define the request model using Pydantic
class UserInput(BaseModel):
    input: str

@app.post("/ask")
async def ask_nero(user_input: UserInput):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": user_input.input
            }
        ],
        max_tokens=150
    )
    return {"response": response.choices[0].message.content.strip()}

@app.get("/")
async def home():
    return {"message": "Welcome to NERO Backend"}

'''
'''import os
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# Load your API key from environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

@app.route('/ask', methods=['POST'])
def ask_nero():
    user_input = request.json.get('input')
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": user_input
            }
        ],
        max_tokens=150
    )
    return jsonify({'response': response.choices[0].message.content.strip()})

@app.route('/')
def home():
    return "Welcome to NERO Backend"
if __name__ == '__main__':
    app.run(debug=True)
'''
'''import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from datetime import datetime

# Load environment variables
load_dotenv()

# Define your FastAPI app
app = FastAPI()

# Load your API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Please check your environment variables.")
client = OpenAI(api_key=api_key)

# Database setup
engine = create_engine('sqlite:///nero.db')
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

# Task Model
class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)

Base.metadata.create_all(bind=engine)

# Scheduler setup
scheduler = BackgroundScheduler()
scheduler.start()

# JWT settings
class Settings(BaseModel):
    authjwt_secret_key: str = "secret"

@AuthJWT.load_config
def get_config():
    return Settings()

# Exception handler for auth errors
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request, exc):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

# Define the request model using Pydantic
class UserInput(BaseModel):
    input: str

# Endpoint to interact with OpenAI API
@app.post("/ask")
async def ask_nero(user_input: UserInput):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": user_input.input
                }
            ],
            max_tokens=150
        )
        return {"response": response.choices[0].message['content'].strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to add a task with database support
@app.post("/tasks")
async def add_task(description: str):
    new_task = Task(description=description)
    db.add(new_task)
    db.commit()
    return {"message": "Task added successfully."}

# Scheduler example function
def scheduled_task():
    print(f"Scheduled task executed at {datetime.now()}")

scheduler.add_job(scheduled_task, 'interval', minutes=10)

# Email notification function
def send_email(to_email: str, subject: str, body: str):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all([smtp_server, smtp_port, smtp_user, smtp_password]):
        raise RuntimeError("SMTP settings are not properly configured.")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = to_email

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.sendmail(smtp_user, to_email, msg.as_string())

# Endpoint to send email notification
@app.post("/send-email")
async def email_notification(to_email: str, subject: str, body: str):
    try:
        send_email(to_email, subject, body)
        return {"message": "Email sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint for JWT login
class UserRequest(BaseModel):
    username: str
    password: str

@app.post("/login")
def login(user: UserRequest, Authorize: AuthJWT = Depends()):
    # Dummy user validation
    if user.username == "valid_user" and user.password == "valid_password":
        access_token = Authorize.create_access_token(subject=user.username)
        return {"access_token": access_token}
    raise HTTPException(status_code=401, detail="Invalid username or password")

@app.get("/")
async def home():
    return {"message": "Welcome to NERO Backend"}
'''
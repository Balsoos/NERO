import uvicorn

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

'''import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from openai import OpenAI
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from fastapi_jwt_auth import AuthJWT
from datetime import datetime, timedelta
import uvicorn
from app import app  # Import the FastAPI app

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
# Load environment variables
load_dotenv()

# FastAPI app setup
app = FastAPI()

# Load OpenAI API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

# Pydantic model for user input
class UserRequest(BaseModel):
    input: str

# Endpoint to interact with OpenAI API
@app.post('/ask')
async def ask_nero(request: UserRequest):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": request.input
            }
        ],
        max_tokens=150
    )
    return {"response": response.choices[0].message['content'].strip()}

# Endpoint to add a task with database storage
@app.post('/add_task')
async def add_task(request: UserRequest, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()  # Require valid JWT for access
    new_task = Task(description=request.input)
    db.add(new_task)
    db.commit()
    return {"status": "success", "task": request.input}

# Function to send email notifications
def send_email_notification(to_email, subject, body):
    email_address = os.getenv("EMAIL_ADDRESS")
    email_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = email_address
    msg['To'] = to_email

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(email_address, email_password)
        server.sendmail(msg['From'], [msg['To']], msg.as_string())

# Endpoint to set a reminder with email notification
@app.post('/set_reminder')
async def set_reminder(request: UserRequest):
    # Assuming the input is formatted as "email, datetime, message"
    try:
        email, reminder_time, message = request.input.split(', ')
        run_date = datetime.strptime(reminder_time, "%Y-%m-%d %H:%M:%S")
        scheduler.add_job(send_email_notification, 'date', run_date=run_date, args=[email, 'Reminder', message])
        return {"status": "reminder set", "message": message}
    except ValueError:
        return {"error": "Invalid input format. Use 'email, datetime, message'"}

# Endpoint for user login to obtain JWT
@app.post('/login')
def login(user: UserRequest, Authorize: AuthJWT = Depends()):
    # Dummy user validation
    if user.input == "valid_user":
        access_token = Authorize.create_access_token(subject="user_id")
        return {"access_token": access_token}
    return {"error": "Invalid user"}


'''
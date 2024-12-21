from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Load OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set. Please check your environment variables.")
client = OpenAI(api_key=api_key)

# Google Calendar setup
credentials = service_account.Credentials.from_service_account_file(
    os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE"), scopes=["https://www.googleapis.com/auth/calendar"]
)
calendar_service = build('calendar', 'v3', credentials=credentials)

# Models
class Event(BaseModel):
    summary: str
    start: str  # Format: YYYY-MM-DDTHH:MM:SS
    end: str    # Format: YYYY-MM-DDTHH:MM:SS

def create_google_calendar_event(event: Event):
    event_body = {
        "summary": event.summary,
        "start": {"dateTime": event.start, "timeZone": "UTC"},
        "end": {"dateTime": event.end, "timeZone": "UTC"},
    }
    return calendar_service.events().insert(calendarId='primary', body=event_body).execute()

# Routes
@app.get("/")
def home():
    return {"message": "Welcome to NERO AI Personal Assistant"}

@app.post("/create-event")
def create_event(event: Event):
    try:
        result = create_google_calendar_event(event)
        return {"message": "Event created successfully", "event_id": result.get("id")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create event: {e}")

class UserQuery(BaseModel):
    query: str

@app.post("/ask-nero")
async def ask_nero(query: UserQuery):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": query.query}
            ],
            max_tokens=150
        )
        return {"response": response.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")

# Voice interaction placeholder (to be implemented)
@app.post("/voice-input")
def voice_input():
    return {"message": "Voice input feature is under development."}

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, field_validator
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
from typing import List
import logging
from datetime import datetime
# Initialize logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

try:
    credentials = service_account.Credentials.from_service_account_file(
        os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE"), scopes=["https://www.googleapis.com/auth/calendar"]
    )
    calendar_service = build('calendar', 'v3', credentials=credentials)
    logger.info("Google Calendar API initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Google Calendar API: {e}")
    raise HTTPException(status_code=500, detail="Google Calendar API initialization failed")

class Event(BaseModel):
    summary: str
    start: str  # Format: YYYY-MM-DDTHH:MM:SS
    end: str    # Format: YYYY-MM-DDTHH:MM:SS

# Add validation to ensure proper date-time format
    @field_validator("start", "end", mode="before")
    def validate_datetime(cls, value):
        try:
            from datetime import datetime
            # Append ":00" if seconds are missing
            if len(value) == 16:  # Format is "YYYY-MM-DDTHH:MM"
                value += ":00"
            datetime.strptime(value, "%Y-%m-%dT%H:%M:%S")
            return value
        except ValueError:
            raise ValueError(f"{value} is not in the correct format: YYYY-MM-DDTHH:MM:SS")

@router.post("/create-event")
def create_event(event: Event):
    try:
        logger.info(f"Creating event: {event}")
        event_body = {
            "summary": event.summary,
            "start": {"dateTime": event.start, "timeZone": "America/Los_Angeles"},
            "end": {"dateTime": event.end, "timeZone": "America/Los_Angeles"},
        }
        result = calendar_service.events().insert(
            calendarId="0c3714955608c6378f9068fe1f04b2de917ca9438c70bf0befbd16fdd6f7495e@group.calendar.google.com", 
            body=event_body
            ).execute()
        logger.info(f"Event created successfully: {result}")
        return {"message": "Event created successfully", "event_id": result.get("id")}
    except Exception as e:
        logger.error(f"Failed to create event: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to create event: {e}")

@router.get("/", response_model=List[Event])
def get_events():
    try:
        events_result = calendar_service.events().list(
            calendarId="0c3714955608c6378f9068fe1f04b2de917ca9438c70bf0befbd16fdd6f7495e@group.calendar.google.com",
            timeMin=datetime.utcnow().isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime",
        ).execute()
        events = events_result.get("items", [])
        return [{"id": e["id"], "summary": e["summary"], "start": e["start"]["dateTime"], "end": e["end"]["dateTime"]} for e in events]
    except Exception as e:
        logger.error(f"Failed to fetch events: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch events: {e}")
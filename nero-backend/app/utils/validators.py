from typing import Any
from fastapi import HTTPException, status
import re
from datetime import datetime

def validate_email(email: str):
    """Validate email format."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format."
        )
    return True

def validate_date(date: str):
    """Validate if the given string is a valid date."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD."
        )
    return True

def validate_priority(priority: str):
    """Validate task priority (low, medium, high)."""
    valid_priorities = ["low", "medium", "high"]
    if priority.lower() not in valid_priorities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid priority. Choose from 'low', 'medium', 'high'."
        )
    return True

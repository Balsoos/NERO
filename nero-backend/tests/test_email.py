from fastapi import APIRouter
from app.services.email import send_email

router = APIRouter()

@router.get("/test-email")
def test_email():
    try:
        send_email("recipient@example.com", "Test Email", "This is a test email from NERO.")
        return {"message": "Test email sent successfully!"}
    except Exception as e:
        return {"error": str(e)}

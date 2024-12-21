from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db.database import SessionLocal
from app.models import Chat, User
from app.auth import get_db
from openai import OpenAI
import pyttsx3
import os

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class ChatRequest(BaseModel):
    user_id: int
    message: str

@router.post("/chat")
def chat_with_nero(request: ChatRequest, db: Session = Depends(get_db)):
    # Validate the user_id
    user = db.query(User).filter(User.id == request.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Save the user's message in the database
    chat = Chat(user_id=request.user_id, message=request.message)
    db.add(chat)
    db.commit()

    # Interact with OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": request.message}],
            max_tokens=150,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

    # Save the AI's reply in the database
    ai_reply = Chat(user_id=request.user_id, message=reply)
    db.add(ai_reply)
    db.commit()

    return {"user_message": request.message, "ai_reply": reply}
# Initialize TTS engine
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 150)  # Set speaking speed

@router.post("/voice-input")
def voice_input():
    # Initialize the recognizer
    recognizer = sr.Recognizer()

    try:
        # Capture audio from microphone
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            print("Processing...")

            # Recognize speech using Google Web API (or other backends)
            user_query = recognizer.recognize_google(audio)
            print(f"User said: {user_query}")

            # Pass user query to the AI chat function (reuse the /chat endpoint logic)
            response = f"NERO's response to '{user_query}' would go here."
            # Convert the response to speech
            tts_engine.say(response)
            tts_engine.runAndWait()

            return {"user_query": user_query, "response": response}

    except sr.UnknownValueError:
        raise HTTPException(status_code=400, detail="Sorry, I could not understand the audio.")
    except sr.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error with speech recognition service: {e}")
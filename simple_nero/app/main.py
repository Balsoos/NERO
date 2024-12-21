from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.auth import router as auth_router
from app.chat import router as chat_router
from app.events import router as events_router
from app.tasks import router as tasks_router
from db.database import init_db
from contextlib import asynccontextmanager

app = FastAPI()
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialization code here
    yield
    # Cleanup code here

app = FastAPI(lifespan=lifespan)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth_router, prefix="/auth")
app.include_router(chat_router, prefix="/chat")
app.include_router(events_router, prefix="/events")
app.include_router(tasks_router, prefix="/tasks")

@app.get("/")
def home():
    return {"message": "Welcome to NERO AI Personal Assistant"}

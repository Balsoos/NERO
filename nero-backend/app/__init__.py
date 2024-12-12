from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.tasks import router as tasks_router
from app.routes.openai import router as openai_router
from app.database import Base, engine
from app.routes import test_reminder
from app.routes import preferences

# Initialize database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Include all routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])
app.include_router(openai_router, prefix="/openai", tags=["openai"])
app.include_router(test_reminder.router, prefix="/test", tags=["test"])
app.include_router(preferences.router, prefix="/preferences", tags=["preferences"])

for route in app.router.routes:
    print(route.path, route.name)

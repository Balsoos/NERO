import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Task, User
from db.database import SessionLocal, Base, engine
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)
@pytest.fixture(scope="function")
def setup_db():
    """
    Fixture to initialize and teardown the test database.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop all tables after the test
        Base.metadata.drop_all(bind=engine)
        
def test_create_task(setup_db):
    """
    Test creating a task with a logged-in user.
    """
    # Generate a valid bcrypt hash for the password
    hashed_password = pwd_context.hash("password123")

    # Insert a test user with the hashed password
    setup_db.execute(
        text("INSERT INTO users (username, hashed_password) VALUES (:username, :hashed_password)"),
        {"username": "testuser", "hashed_password": hashed_password}
    )
    setup_db.commit()

    # Log in as the test user to get a token
    token_response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert token_response.status_code == 200

    token = token_response.json()["access_token"]

    # Create a new task
    task_data = {"description": "Test Task", "priority": "high", "due_date": "2024-12-25T00:00:00"}
    response = client.post(
        "/tasks/",
        json=task_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["description"] == "Test Task"


def test_get_tasks(setup_db):
    """
    Test retrieving tasks for a logged-in user.
    """
    # Generate a valid bcrypt hash for the password
    hashed_password = pwd_context.hash("password123")

    # Insert a test user with the hashed password
    setup_db.execute(
        text("INSERT INTO users (username, hashed_password) VALUES (:username, :hashed_password)"),
        {"username": "testuser", "hashed_password": hashed_password}
    )
    setup_db.commit()

    # Log in as the test user to get a token
    token_response = client.post("/auth/login", json={"username": "testuser", "password": "password123"})
    assert token_response.status_code == 200

    token = token_response.json()["access_token"]

    # Fetch tasks for the logged-in user
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
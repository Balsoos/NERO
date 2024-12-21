import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.main import app
from fastapi.testclient import TestClient
from passlib.context import CryptContext

# Test database configuration
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

client = TestClient(app)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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


def test_create_event(setup_db):
    """
    Test creating an event with a logged-in user.
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

    # Create an event using the token
    event_data = {
        "summary": "Test Event",
        "start": "2024-12-21T10:00:00",
        "end": "2024-12-21T11:00:00",
    }
    response = client.post(
        "/events/create-event",
        json=event_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Event created successfully"
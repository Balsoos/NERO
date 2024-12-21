import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import User
from app.main import app
from db.database import Base

# Test database URL
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"

# Test database engine and session
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a FastAPI test client
client = TestClient(app)

@pytest.fixture(scope="function")
def setup_db():
    """
    Fixture to set up and tear down the test database.
    """
    # Create the database schema
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop the database schema after the test
        Base.metadata.drop_all(bind=engine)

def test_register(setup_db):
    """
    Test the /auth/register endpoint.
    """
    # Ensure the user does not already exist
    setup_db.query(User).filter_by(username="testuser").delete()
    setup_db.commit()

    # Send a POST request to register a new user
    response = client.post("/auth/register", json={"username": "testuser1", "password": "1password123"})
    assert response.status_code == 200
    assert response.json()["message"] == "User registered successfully"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.database import Base

# Create an in-memory SQLite database for tests
@pytest.fixture(scope="function")
def setup_db():
    engine = create_engine("sqlite:///:memory:")  # In-memory database for isolation
    Base.metadata.create_all(bind=engine)  # Create tables
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db  # Provide the session to the test
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)  # Drop tables after test

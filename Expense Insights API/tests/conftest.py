import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test_expense_insights.db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    if os.path.exists("./test_expense_insights.db"):
        os.remove("./test_expense_insights.db")
        
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(name="client")
def client_fixture(session):
    def override_get_db():
        try:
            yield session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    
    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
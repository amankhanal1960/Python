import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Base, get_db, sessionmaker

from app.database import Base, get_db
from app.main import app

@pytest.fixture
def test_engine(tmp_path):
    db_path = tmp_path / "test_expense_insights.db"
    
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False}
    )
    
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    
@pytest.fixture(name="client")
def client_fixture(test_engine):
    
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_engine
    )
    
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    from fastapi.testclient import TestClient
    
    with TestClient(app) as test_client:
        yield test_client
        
    app.dependency_overrides.pop(get_db, None)
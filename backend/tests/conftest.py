import sys
import os 
from pathlib import Path

backend_dir = Path(__file__).resolve().parent.parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))


os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["GOOGLE_API_KEY"] = "mock-test-key-for-local-tests"
os.environ["JWT_SECRET_KEY"] = "super-secret-sales-agent-test-key-32bytes-min"

import pytest 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

# Using in-memory SQLite database for ultra-fast , isolated testing
SQLITE_TEST_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLITE_TEST_URL,
    connect_args={"check_same_thread":False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

from database.base import Base
from database.dependencies import get_db
from models.business import Business
from models.product import Product
from models.policy import Policy
from models.customer import Customer
from models.order import Order
from models.admin import Admin

@pytest.fixture(scope="function")
def db_session():
    """
    Creates fresh database tables in RAM before each test,
    yields the session, and drops tables after the test finishes.
    """
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    FastApi TestClient with the database dependency overridden
    to use our test SQLite database instead of production postgres.
    """
    from main import app

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
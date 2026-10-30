import os
import uuid

os.environ.setdefault("SECRET_KEY", "testsecret")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import Base, get_db
from main import app


@pytest.fixture()
def client():
    """Клиент с чистой in-memory БД на каждый тест."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    engine.dispose()


@pytest.fixture()
def make_user(client):
    """Регистрирует нового пользователя и возвращает заголовок авторизации."""

    def _make_user():
        email = f"{uuid.uuid4().hex}@example.com"
        client.post("/auth/register", json={"email": email, "password": "password123"})
        login = client.post("/auth/login", json={"email": email, "password": "password123"})
        return {"Authorization": f"Bearer {login.json()['access_token']}"}

    return _make_user

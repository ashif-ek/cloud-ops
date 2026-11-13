
import pytest

from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.routes import router
from app.db.database import Base, get_db
from app.db import models


test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)

application_under_test = FastAPI()
application_under_test.include_router(router)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


application_under_test.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    with TestClient(application_under_test) as test_client:
        yield test_client

    Base.metadata.drop_all(bind=test_engine)


def test_create_task(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Learn Docker",
            "description": "Understand containers",
        },
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Learn Docker"
    assert response.json()["completed"] is False


def test_get_tasks(client):
    client.post(
        "/tasks",
        json={"title": "Learn Python"},
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Learn Docker"},
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    assert response.status_code == 200
    assert response.json()["completed"] is True


def test_delete_task(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Temporary task"},
    )

    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_get_nonexistent_task(client):
    response = client.get("/tasks/9999")

    assert response.status_code == 404

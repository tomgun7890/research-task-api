import sqlite3

import pytest
import database

from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_test_db(tmp_path, monkeypatch):
    test_db = tmp_path / "test_tasks.db"

    monkeypatch.setattr(
        database,
        "DB_PATH",
        str(test_db)
    )

    connection = sqlite3.connect(test_db)
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE tasks (" \
        "id INTEGER PRIMARY KEY," \
        "title TEXT NOT NULL," \
        "status TEXT NOT NULL" \
        ")"
    )

    cursor.execute(
        "INSERT INTO tasks (title, status) VALUES (?, ?)",
        ("Read paper", "todo")
    )

    cursor.execute(
        "INSERT INTO tasks (title, status) VALUES (?, ?)",
        ("Run experiment", "done")
    )

    connection.commit()
    connection.close()

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_get_missing_task():
    response = client.get("/tasks/9999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Task not found"}

def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Write paper",
            "status": "todo"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 3,
        "title": "Write paper",
        "status": "todo"
    }

    get_response = client.get("/tasks/3")

    assert get_response.status_code == 200
    assert get_response.json() == {
        "id": 3,
        "title": "Write paper",
        "status": "todo"
    }

def test_update_task():
    response = client.patch(
        "/tasks/1",
        json={
            "status": "done"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Read paper",
        "status": "done"
    }

    get_response = client.get("/tasks/1")

    assert get_response.status_code == 200
    assert get_response.json() == {
        "id": 1,
        "title": "Read paper",
        "status": "done"
    }

def test_delete_task():
    response = client.delete("/tasks/1")

    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted"}

    get_response = client.get("/tasks/1")

    assert get_response.status_code == 404
    assert get_response.json() == {"detail": "Task not found"}
from unittest.mock import Mock
import pytest
from fastapi.testclient import TestClient
from src.bmodels import Task
from src.app import app, get_db

client = TestClient(app)

@pytest.fixture
def test_get_db():
    # mock = MockDB()
    return Mock(spec=["session", "query", "add", "commit", "close"])

def test_show_tasks(test_get_db):
    # Mock the database
    app.dependency_overrides[get_db] = test_get_db
    mock_db = test_get_db
    mock_task = Task(title="Mock Task", description="Mock Description", due_date="2023-12-01")
    mock_db.session.query.return_value.all.return_value = [mock_task]

    # Perform the test
    response = client.get("/tasks/")

    if response.status_code == 422:
        print(response.content)

    assert response.status_code == 200
    assert response.json() == [mock_task.model_dump()]

    # Clean up
    app.dependency_overrides.clear()
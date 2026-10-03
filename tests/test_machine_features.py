from datetime import date, timedelta

import pytest
from fastapi.testclient import TestClient

import src.storage as storage
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(storage, "DATABASE_PATH", tmp_path / "records.sqlite3")
    with TestClient(app) as test_client:
        yield test_client


def test_prediction_is_saved_to_machine_history(client):
    response = client.post(
        "/predict",
        json={
            "machine_id": "press-7",
            "machine_type": "L",
            "air_temperature": 300,
            "process_temperature": 310,
            "rotational_speed": 1500,
            "torque": 50,
            "tool_wear": 100,
        },
    )

    assert response.status_code == 200
    assert response.json()["possible_failure_modes"]

    history = client.get("/machines/press-7/history")
    assert history.status_code == 200
    assert len(history.json()) == 1
    assert history.json()[0]["air_temperature"] == 300


def test_maintenance_reminder_is_saved_for_machine(client):
    last_serviced_on = date.today().isoformat()
    response = client.put(
        "/machines/press-7/maintenance",
        json={"last_serviced_on": last_serviced_on, "interval_days": 30},
    )

    assert response.status_code == 200
    assert response.json()["machine_id"] == "press-7"
    assert response.json()["due_date"] == (
        date.today() + timedelta(days=30)
    ).isoformat()

    saved = client.get("/machines/press-7/maintenance")
    assert saved.status_code == 200
    assert saved.json()["interval_days"] == 30


def test_future_service_date_is_rejected(client):
    response = client.put(
        "/machines/press-7/maintenance",
        json={"last_serviced_on": "2999-01-01", "interval_days": 30},
    )

    assert response.status_code == 400
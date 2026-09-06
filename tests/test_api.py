from datetime import date, timedelta
from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "WeatherGPT API is running"


def test_query_valid_request():
    response = client.post(
        "/query",
        json={
            "message": "When should I spray my tomato crop tomorrow?",
            "latitude": 28.67,
            "longitude": 77.43
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["activity"] == "spraying"
    assert data["crop"] == "tomato"
    expected_date = (date.today() + timedelta(days=1)).isoformat()       
    assert data["date"] == expected_date
    assert data["latitude"] == 28.67
    assert data["longitude"] == 77.43
    assert data["is_valid"] is True

    
def test_query_missing_crop():
    response = client.post(
        "/query",
        json={
            "message": "Can I spray tomorrow?",
            "latitude": 28.67,
            "longitude": 77.43
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["activity"] == "spraying"
    assert data["crop"] is None

    expected_date = (date.today() + timedelta(days=1)).isoformat()
    assert data["date"] == expected_date
    
    assert "crop" in data["missing_fields"]
    assert data["is_valid"] is False

def test_query_with_time():
    response = client.post(
        "/query",
        json={
            "message": "Can I spray my tomato crop tomorrow at 7 PM?",
            "latitude": 28.67,
            "longitude": 77.43
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["activity"] == "spraying"
    assert data["crop"] == "tomato"

    expected_date = (date.today() + timedelta(days=1)).isoformat()
    assert data["date"] == expected_date

    assert data["time"] == "7 PM"
    assert data["is_valid"] is True

def test_query_empty_message():
    response = client.post(
        "/query",
        json={
            "message": "",
            "latitude": 28.67,
            "longitude": 77.43
        }
    )

    assert response.status_code == 422


def test_query_invalid_latitude():
    response = client.post(
        "/query",
        json={
            "message": "What is the weather tomorrow?",
            "latitude": 100,
            "longitude": 77.43
        }
    )

    assert response.status_code == 422


def test_query_invalid_longitude():
    response = client.post(
        "/query",
        json={
            "message": "What is the weather tomorrow?",
            "latitude": 28.67,
            "longitude": 200
        }
    )

    assert response.status_code == 422


def test_query_without_location():
    response = client.post(
        "/query",
        json={
            "message": "What is the weather tomorrow?"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["latitude"] is None
    assert data["longitude"] is None
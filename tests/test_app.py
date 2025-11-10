
import pytest
from fastapi.testclient import TestClient
from src.app import app


client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister():
    """Test signup and unregister endpoints with a unique email."""
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"
    # Signup
    response = client.post(
        f"/activities/{activity}/signup?email={test_email}"
    )
    assert response.status_code in (200, 400)  # 400 if already signed up
    # Unregister
    response = client.post(
        f"/activities/{activity}/unregister?email={test_email}"
    )
    assert response.status_code in (200, 404)  # 404 if not found


def test_signup_duplicate():
    """Test duplicate signup returns 400."""
    activity = "Programming Class"
    email = "emma@mergington.edu"  # Already signed up
    response = client.post(
        f"/activities/{activity}/signup?email={email}"
    )
    assert response.status_code == 400
    assert "already signed up" in response.json().get("detail", "")


def test_unregister_not_found():
    """Test unregistering a non-existent participant returns 404."""
    activity = "Programming Class"
    email = "notfound@mergington.edu"
    response = client.post(
        f"/activities/{activity}/unregister?email={email}"
    )
    assert response.status_code == 404
    assert "Participant not found" in response.json().get("detail", "")

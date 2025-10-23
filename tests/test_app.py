import copy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def isolate_activities():
    # Make a deep copy of activities and restore after test to avoid cross-test pollution
    original = copy.deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


@pytest.fixture()
def client():
    return TestClient(app_module.app)


def test_signup_and_unregister_flow(client):
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure the test email is not present
    if email in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].remove(email)

    # Signup via query param
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in app_module.activities[activity]["participants"]

    # Unregister via JSON body
    resp = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert resp.status_code == 200
    assert email not in app_module.activities[activity]["participants"]


def test_unregister_missing_email_returns_400(client):
    activity = "Chess Club"
    resp = client.post(f"/activities/{activity}/unregister", json={})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Missing email to unregister"


def test_cannot_unregister_nonparticipant(client):
    activity = "Chess Club"
    email = "not-in-list@example.com"
    resp = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Participant not found in activity"


def test_duplicate_signup_returns_400(client):
    activity = "Chess Club"
    email = "dup@example.com"

    # Ensure clean state
    if email in app_module.activities[activity]["participants"]:
        app_module.activities[activity]["participants"].remove(email)

    # First signup ok
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200

    # Second signup should fail
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Student is already signed up"

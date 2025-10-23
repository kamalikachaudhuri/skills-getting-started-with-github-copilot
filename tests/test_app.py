from fastapi.testclient import TestClient
from src.app import app, activities


client = TestClient(app)


def test_signup_and_unregister_flow():
    activity = "Chess Club"
    email = "testuser@example.com"

    # Ensure the test email is not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup via query param
    resp = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Unregister via JSON body
    resp = client.post(f"/activities/{activity}/unregister", json={"email": email})
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_missing_email_returns_400():
    activity = "Chess Club"
    resp = client.post(f"/activities/{activity}/unregister", json={})
    assert resp.status_code == 400
    assert resp.json()["detail"] == "Missing email to unregister"

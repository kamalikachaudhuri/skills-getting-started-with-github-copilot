"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException, Body, Query
from pydantic import BaseModel, ValidationError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Competitive soccer practices and matches against other schools",
        "schedule": "Mondays, Wednesdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Pickup games, drills, and intramural tournaments",
        "schedule": "Tuesdays and Thursdays, 5:00 PM - 7:00 PM",
        "max_participants": 18,
        "participants": ["ava@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore drawing, painting, and mixed media projects",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["mia@mergington.edu", "charlotte@mergington.edu"]
    },
    "Drama Club": {
        "description": "Acting workshops, play production, and stagecraft",
        "schedule": "Fridays, 4:00 PM - 6:30 PM",
        "max_participants": 25,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments, guest lectures, and science fairs",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["ethan@mergington.edu", "lucas@mergington.edu"]
    },
    "Debate Team": {
        "description": "Practice persuasive speaking, research, and competitive debates",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 14,
        "participants": ["sophomore1@mergington.edu", "junior1@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


class SignupRequest(BaseModel):
    email: str


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(
    activity_name: str,
    email: str | None = Query(None, description="Student email as query parameter"),
    payload: dict | None = Body(None),
):
    """Sign up a student for an activity.

    Accepts email either as a query parameter (?email=) or as a JSON body
    {"email": "..."}. Uses EmailStr for validation.
    """
    # Resolve email from either query param or JSON body
    if not email and payload is not None:
        # allow payload to be a dict (client may send empty JSON {})
        try:
            # payload may already be a dict; parse and validate
            parsed = SignupRequest.parse_obj(payload)
            email = parsed.email
        except ValidationError:
            # Keep behavior: if body missing email, return 400
            raise HTTPException(status_code=400, detail="Missing email to sign up")

    if not email:
        raise HTTPException(status_code=400, detail="Missing email to sign up")

    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student is already signed up")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


class UnregisterRequest(BaseModel):
    email: str

@app.post("/activities/{activity_name}/unregister")
def unregister_from_activity(
    activity_name: str,
    email: str | None = Query(None, description="Student email as query parameter"),
    payload: dict | None = Body(None),
):
    """Unregister a student from an activity by email (POST body or query param).

    Accepts the email either as a query parameter (e.g. ?email=...) or
    in a JSON body like {"email": "user@example.com"}.
    """
    # Resolve email from either query param or JSON body
    if not email and payload is not None:
        try:
            parsed = UnregisterRequest.parse_obj(payload)
            email = parsed.email
        except ValidationError:
            raise HTTPException(status_code=400, detail="Missing email to unregister")

    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    if not email:
        raise HTTPException(status_code=400, detail="Missing email to unregister")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Participant not found in activity")

    activity["participants"].remove(email)
    return {"message": f"Unregistered {email} from {activity_name}"}

"""
Pytest configuration and fixtures for FastAPI backend tests.

Provides:
- TestClient fixture for making HTTP requests to the app
- Fixtures for test data and participants
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


# Store the initial activities state for resetting between tests
INITIAL_ACTIVITIES = {
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
    "Basketball Team": {
        "description": "Practice and compete in basketball games",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Soccer Club": {
        "description": "Train and play soccer matches",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 5:00 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore painting, drawing, and other visual arts",
        "schedule": "Mondays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["isabella@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act in plays and learn theater skills",
        "schedule": "Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 20,
        "participants": ["mason@mergington.edu", "charlotte@mergington.edu"]
    },
    "Debate Club": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["ethan@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Tuesdays, 3:00 PM - 4:30 PM",
        "max_participants": 25,
        "participants": ["harper@mergington.edu", "logan@mergington.edu"]
    }
}


@pytest.fixture
def client():
    """Provide a TestClient instance for testing the FastAPI app.
    
    Resets the app's activities to initial state before each test to ensure test isolation.
    """
    from src import app as app_module
    
    # Reset activities to initial state
    app_module.activities.clear()
    for activity_name, activity_data in INITIAL_ACTIVITIES.items():
        app_module.activities[activity_name] = {
            **activity_data,
            "participants": activity_data["participants"].copy()
        }
    
    return TestClient(app)


@pytest.fixture
def test_activity_name():
    """Provide a test activity name that exists in the app."""
    return "Chess Club"


@pytest.fixture
def test_participant_email():
    """Provide a test participant email that is not pre-loaded."""
    return "test.participant@mergington.edu"


@pytest.fixture
def test_nonexistent_activity():
    """Provide a non-existent activity name for error testing."""
    return "Nonexistent Club"

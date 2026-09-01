"""
Shared test fixtures and configuration for FastAPI backend tests.
"""
import pytest
from fastapi.testclient import TestClient
import src.app as app_module


# Test email constants
TEST_EMAIL_1 = "test_student_1@mergington.edu"
TEST_EMAIL_2 = "test_student_2@mergington.edu"
TEST_EMAIL_3 = "test_student_3@mergington.edu"


# Store original activities state
ORIGINAL_ACTIVITIES = {
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
        "description": "Competitive basketball team with training and games",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu", "james@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis instruction and friendly matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
        "max_participants": 10,
        "participants": ["sarah@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Drama Club": {
        "description": "Perform in theatrical productions and develop acting skills",
        "schedule": "Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["noah@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop argumentation and public speaking skills",
        "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 12,
        "participants": ["avery@mergington.edu", "jordan@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific discoveries",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["mia@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """
    Reset the activities dict to its original state before each test.
    This ensures tests are isolated and don't affect each other.
    """
    # Reset to original state by deep copying the activities
    app_module.activities.clear()
    for key, value in ORIGINAL_ACTIVITIES.items():
        app_module.activities[key] = {
            **value,
            "participants": value["participants"][:]  # Create a new list copy
        }
    yield


@pytest.fixture
def client():
    """
    Provide a TestClient instance for making requests to the FastAPI app.
    This client uses the in-memory database.
    """
    return TestClient(app_module.app)


@pytest.fixture
def sample_activity():
    """
    Provide a sample activity dict for test setup/verification.
    """
    return {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        }
    }


@pytest.fixture
def valid_activity_name():
    """Provide a valid activity name that exists in the test app."""
    return "Chess Club"


@pytest.fixture
def invalid_activity_name():
    """Provide an invalid activity name that does not exist."""
    return "Nonexistent Club"

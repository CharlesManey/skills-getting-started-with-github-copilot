"""
Tests for the GET /activities endpoint.
"""
import pytest


def test_get_activities_success(client):
    """
    Test that GET /activities returns all activities with correct structure.
    """
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify response is a dict
    assert isinstance(data, dict)
    
    # Verify expected activities are present
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_get_activities_contains_required_fields(client):
    """
    Test that each activity has required fields.
    """
    response = client.get("/activities")
    data = response.json()
    
    # Pick an activity to verify structure
    activity = data["Chess Club"]
    
    # Verify required fields
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity


def test_get_activities_participants_list(client):
    """
    Test that participants are returned as a list for each activity.
    """
    response = client.get("/activities")
    data = response.json()
    
    for activity_name, activity_details in data.items():
        assert isinstance(activity_details["participants"], list)


def test_get_activities_contains_participants(client):
    """
    Test that activities with participants show them in the list.
    """
    response = client.get("/activities")
    data = response.json()
    
    # Chess Club should have participants
    chess_club = data["Chess Club"]
    assert len(chess_club["participants"]) > 0
    assert "michael@mergington.edu" in chess_club["participants"]
    assert "daniel@mergington.edu" in chess_club["participants"]

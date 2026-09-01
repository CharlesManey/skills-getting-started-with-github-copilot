"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
"""
import pytest
from tests.conftest import TEST_EMAIL_1, TEST_EMAIL_2


def test_unregister_success(client, valid_activity_name):
    """
    Test that a student can successfully unregister from an activity.
    """
    # First, sign up
    signup_response = client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_1}
    )
    assert signup_response.status_code == 200
    
    # Then unregister
    response = client.delete(
        f"/activities/{valid_activity_name}/unregister",
        params={"email": TEST_EMAIL_1}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert TEST_EMAIL_1 in data["message"]
    assert "Unregistered" in data["message"]


def test_unregister_removes_participant(client, valid_activity_name):
    """
    Test that unregistering removes the participant from the activity's participant list.
    """
    # Sign up
    client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_1}
    )
    
    # Verify participant is in list
    activities = client.get("/activities").json()
    assert TEST_EMAIL_1 in activities[valid_activity_name]["participants"]
    
    # Unregister
    response = client.delete(
        f"/activities/{valid_activity_name}/unregister",
        params={"email": TEST_EMAIL_1}
    )
    assert response.status_code == 200
    
    # Verify participant was removed
    activities = client.get("/activities").json()
    assert TEST_EMAIL_1 not in activities[valid_activity_name]["participants"]


def test_unregister_nonexistent_activity(client, invalid_activity_name):
    """
    Test that unregistering from a nonexistent activity returns 404.
    """
    response = client.delete(
        f"/activities/{invalid_activity_name}/unregister",
        params={"email": TEST_EMAIL_1}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_not_registered_student(client, valid_activity_name):
    """
    Test that unregistering a student who is not registered returns 400.
    """
    response = client.delete(
        f"/activities/{valid_activity_name}/unregister",
        params={"email": TEST_EMAIL_1}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_one_participant_keeps_others(client, valid_activity_name):
    """
    Test that unregistering one participant doesn't affect others.
    """
    # Sign up two students
    client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_1}
    )
    client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_2}
    )
    
    # Unregister first student
    response = client.delete(
        f"/activities/{valid_activity_name}/unregister",
        params={"email": TEST_EMAIL_1}
    )
    assert response.status_code == 200
    
    # Verify first is removed but second remains
    activities = client.get("/activities").json()
    participants = activities[valid_activity_name]["participants"]
    assert TEST_EMAIL_1 not in participants
    assert TEST_EMAIL_2 in participants


def test_unregister_then_signup_again(client, valid_activity_name):
    """
    Test that a student can sign up again after unregistering.
    """
    # Sign up
    client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_1}
    )
    
    # Unregister
    client.delete(
        f"/activities/{valid_activity_name}/unregister",
        params={"email": TEST_EMAIL_1}
    )
    
    # Sign up again - should succeed
    response = client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_1}
    )
    
    assert response.status_code == 200
    
    # Verify student is in participants list
    activities = client.get("/activities").json()
    assert TEST_EMAIL_1 in activities[valid_activity_name]["participants"]

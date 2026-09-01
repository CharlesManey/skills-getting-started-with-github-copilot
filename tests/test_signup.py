"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""
import pytest
from tests.conftest import TEST_EMAIL_1, TEST_EMAIL_2, TEST_EMAIL_3


def test_signup_success(client, valid_activity_name):
    """
    Test that a student can successfully sign up for an activity.
    """
    response = client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_1}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert TEST_EMAIL_1 in data["message"]
    assert valid_activity_name in data["message"]


def test_signup_adds_participant(client, valid_activity_name):
    """
    Test that signing up adds the participant to the activity's participant list.
    """
    # Sign up
    response = client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_1}
    )
    assert response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert TEST_EMAIL_1 in activities[valid_activity_name]["participants"]


def test_signup_nonexistent_activity(client, invalid_activity_name):
    """
    Test that signing up for a nonexistent activity returns 404.
    """
    response = client.post(
        f"/activities/{invalid_activity_name}/signup",
        params={"email": TEST_EMAIL_1}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate_email(client, valid_activity_name):
    """
    Test that signing up with a duplicate email returns 400.
    """
    # First signup - should succeed
    response1 = client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_1}
    )
    assert response1.status_code == 200
    
    # Second signup with same email - should fail
    response2 = client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_1}
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_multiple_students_same_activity(client, valid_activity_name):
    """
    Test that multiple different students can sign up for the same activity.
    """
    # First student
    response1 = client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_1}
    )
    assert response1.status_code == 200
    
    # Second student
    response2 = client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": TEST_EMAIL_2}
    )
    assert response2.status_code == 200
    
    # Verify both are in participants list
    activities_response = client.get("/activities")
    activities = activities_response.json()
    participants = activities[valid_activity_name]["participants"]
    assert TEST_EMAIL_1 in participants
    assert TEST_EMAIL_2 in participants


def test_signup_same_student_different_activities(client):
    """
    Test that a student can sign up for multiple different activities.
    """
    # Sign up for Chess Club
    response1 = client.post(
        "/activities/Chess Club/signup",
        params={"email": TEST_EMAIL_1}
    )
    assert response1.status_code == 200
    
    # Sign up for Programming Class
    response2 = client.post(
        "/activities/Programming Class/signup",
        params={"email": TEST_EMAIL_1}
    )
    assert response2.status_code == 200
    
    # Verify student is in both activities
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert TEST_EMAIL_1 in activities["Chess Club"]["participants"]
    assert TEST_EMAIL_1 in activities["Programming Class"]["participants"]

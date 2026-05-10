"""
Tests for the POST /activities/{activity_name}/signup endpoint.

Tests student signup for activities including happy path and error cases.
"""


def test_signup_valid_participant_succeeds(client, test_activity_name, test_participant_email):
    """Test that a valid signup adds the participant to the activity."""
    # Arrange
    activity_name = test_activity_name
    email = test_participant_email
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_signup_multiple_participants_same_activity(client, test_activity_name):
    """Test that multiple different participants can sign up for the same activity."""
    # Arrange
    activity_name = test_activity_name
    email1 = "participant1@mergington.edu"
    email2 = "participant2@mergington.edu"
    
    # Act
    response1 = client.post(
        f"/activities/{activity_name}/signup?email={email1}"
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup?email={email2}"
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    
    # Verify both are in the activity
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email1 in activities[activity_name]["participants"]
    assert email2 in activities[activity_name]["participants"]


def test_signup_activity_not_found_returns_404(client, test_participant_email, test_nonexistent_activity):
    """Test that signing up for a non-existent activity returns 404."""
    # Arrange
    activity_name = test_nonexistent_activity
    email = test_participant_email
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_already_signed_up_returns_400(client, test_activity_name):
    """Test that a participant already signed up cannot sign up again."""
    # Arrange
    activity_name = test_activity_name
    email = "michael@mergington.edu"  # Already signed up for Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already signed up" in data["detail"].lower()


def test_signup_same_participant_twice_returns_400(client, test_activity_name, test_participant_email):
    """Test that the same participant cannot sign up twice."""
    # Arrange
    activity_name = test_activity_name
    email = test_participant_email
    
    # Act - First signup should succeed
    response1 = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Act - Second signup with same email should fail
    response2 = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    assert "already signed up" in response2.json()["detail"].lower()

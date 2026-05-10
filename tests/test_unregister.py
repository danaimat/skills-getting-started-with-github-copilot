"""
Tests for the POST /activities/{activity_name}/unregister endpoint.

Tests student unregistration from activities including happy path and error cases.
"""


def test_unregister_valid_participant_succeeds(client, test_activity_name):
    """Test that a valid unregister removes the participant from the activity."""
    # Arrange
    activity_name = test_activity_name
    email = "michael@mergington.edu"  # Pre-loaded in Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert email in data["message"]
    assert activity_name in data["message"]


def test_unregister_removes_participant_from_activity(client, test_activity_name):
    """Test that unregistering actually removes the participant from the activity."""
    # Arrange
    activity_name = test_activity_name
    email = "michael@mergington.edu"
    
    # Act
    client.post(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert - Verify participant is no longer in the activity
    response = client.get("/activities")
    activities = response.json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_participant_can_re_signup(client, test_activity_name):
    """Test that a participant can sign up again after unregistering."""
    # Arrange
    activity_name = test_activity_name
    email = "michael@mergington.edu"
    
    # Act - Unregister
    unregister_response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Act - Re-signup
    signup_response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )
    
    # Assert
    assert unregister_response.status_code == 200
    assert signup_response.status_code == 200
    
    # Verify participant is back in the activity
    response = client.get("/activities")
    activities = response.json()
    assert email in activities[activity_name]["participants"]


def test_unregister_activity_not_found_returns_404(client, test_participant_email, test_nonexistent_activity):
    """Test that unregistering from a non-existent activity returns 404."""
    # Arrange
    activity_name = test_nonexistent_activity
    email = test_participant_email
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_participant_not_signed_up_returns_400(client, test_activity_name, test_participant_email):
    """Test that unregistering when not signed up returns 400."""
    # Arrange
    activity_name = test_activity_name
    email = test_participant_email  # Not signed up for Chess Club
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_twice_returns_400(client, test_activity_name):
    """Test that unregistering twice returns an error on the second attempt."""
    # Arrange
    activity_name = test_activity_name
    email = "michael@mergington.edu"
    
    # Act - First unregister should succeed
    response1 = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Act - Second unregister should fail
    response2 = client.post(
        f"/activities/{activity_name}/unregister?email={email}"
    )
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 400
    assert "not signed up" in response2.json()["detail"].lower()

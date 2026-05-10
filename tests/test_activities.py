"""
Tests for the GET /activities endpoint.

Tests the retrieval of all activities from the API.
"""


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all activities in the system."""
    # Arrange
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Basketball Team",
        "Soccer Club", "Art Club", "Drama Club", "Debate Club", "Science Club"
    ]
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert set(activities.keys()) == set(expected_activities)


def test_get_activities_returns_correct_activity_structure(client):
    """Test that each activity has the required fields."""
    # Arrange
    required_fields = {"description", "schedule", "max_participants", "participants"}
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data, dict)
        assert set(activity_data.keys()) == required_fields


def test_get_activities_returns_participants_as_list(client):
    """Test that participants field contains a list of emails."""
    # Arrange
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_data["participants"], list)
        for participant in activity_data["participants"]:
            assert isinstance(participant, str)
            assert "@" in participant  # Basic email validation

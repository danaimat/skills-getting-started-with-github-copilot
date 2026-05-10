"""
Tests for the GET / endpoint.

Tests the root endpoint redirect to static files.
"""


def test_root_redirect_to_static_files(client):
    """Test that the root endpoint redirects to static index.html."""
    # Arrange
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_redirect_location_correct(client):
    """Test that the redirect location is correct."""
    # Arrange
    expected_location = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert "location" in response.headers
    assert response.headers["location"] == expected_location


def test_root_with_follow_redirects(client):
    """Test following the root redirect resolves to the static file."""
    # Arrange
    
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    # After following redirects, we should get a successful response
    assert response.status_code == 200

from unittest.mock import patch


def test_display_points(client):
    """
    Test the display_points route to ensure it renders the display_points.html
    template with the correct club data.
    """
    # Mock club data
    mock_clubs = [
        {"name": "Club 1", "points": "10"},
        {"name": "Club 2", "points": "15"},
        {"name": "Club 3", "points": "5"}
    ]

    # Patch the global `clubs` variable in the server module
    with patch("server.clubs", mock_clubs):
        # Simulate a GET request to the /display-points route
        response = client.get("/display-points")

        # Assert the response status code is 200 (OK)
        assert response.status_code == 200

        # Assert that the template contains the club data
        assert b"Club 1" in response.data
        assert b"Club 2" in response.data
        assert b"Club 3" in response.data
        assert b"10" in response.data
        assert b"15" in response.data
        assert b"5" in response.data

def test_display_points_integration(client):
    """
    Integration test for the /display-points route.
    It ensures that the route renders the correct template and
    passes the correct data for clubs from the temp_clubs_file.
    """
    # Simulate a GET request to the /display-points route
    response = client.get("/display-points")

    # Assert the response status code is 200 (OK)
    assert response.status_code == 200
    print(response.data)
    # Check if the response contains data from the temp_clubs_file
    assert b"Club 1" in response.data
    assert b"Club 2" in response.data
    assert b"5" in response.data
    assert b"15" in response.data

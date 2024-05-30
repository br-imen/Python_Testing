

def test_purchase_places_valid(client):
    """
    Test purchasing places with valid club points and valid competition.
    """
    response = client.post("/purchasePlaces", data={
        "competition": "Competition 1",
        "club": "Club 1",
        "places": "5"
    })

    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data


def test_purchase_places_insufficient_points(client):
    """
    Test purchasing more places than the club's available points.
    """
    response = client.post("/purchasePlaces", data={
        "competition": "Competition 1",
        "club": "Club 1",
        "places": "20"  # Club 1 has only 10 points
    })

    assert response.status_code == 302  # Redirect expected
    response = client.get(response.headers["Location"])  # Follow the redirect
    assert b"Places required exceed club&#39;s total points" in response.data


def test_purchase_places_zero_places(client):
    """
    Test purchasing zero places, which is an invalid input.
    """
    response = client.post("/purchasePlaces", data={
        "competition": "Competition 1",
        "club": "Club 1",
        "places": "0"
    })

    assert response.status_code == 302  # Redirect expected
    response = client.get(response.headers["Location"])  # Follow the redirect
    assert b"Places required must be a positive integer" in response.data

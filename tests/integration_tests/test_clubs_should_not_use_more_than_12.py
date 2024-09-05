
def test_purchase_places_exceeds_12(client):
    """
    Test purchasing more places than 12.
    """
    response = client.post("/purchasePlaces", data={
        "competition": "Competition 1",
        "club": "Club 1",
        "places": "13"
    })

    assert response.status_code == 302  # Redirect expected
    response = client.get(response.headers["Location"])  # Follow the redirect
    assert b"Places required must be a positive integer"
    b" that does not exceed 12" in response.data

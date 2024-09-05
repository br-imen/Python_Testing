import json


def test_purchase_places_valid(client):
    """
    Test purchasing places with valid club points and valid competition.
    """
    response = client.post("/purchasePlaces", data={
        "competition": "Competition 1",
        "club": "Club 1",
        "places": "5"
    })

    # Check the response and verify the club's points were updated
    assert response.status_code == 200
    assert b"Great-booking complete!" in response.data

    with open(client.application.config['CLUB_FILE'], 'r') as f:
        updated_clubs = json.load(f)
        assert updated_clubs["clubs"][0]["points"] == "0"

import json


# Mock data for clubs and competitions
mock_clubs_list = [
    {"name": "Club 1", "email": "club1@example.com", "points": "10"},
    {"name": "Club 2", "email": "club2@example.com", "points": "15"},
]

mock_competitions_list = [
    {
        "name": "Competition 1",
        "date": "2023-03-27 10:00:00",
        "numberOfPlaces": "25",
    },
    {
        "name": "Competition 2",
        "date": "2023-10-22 13:30:00",
        "numberOfPlaces": "15",
    },
]
# Mock data for clubs.json and competitions.json
mock_clubs_json = json.dumps({"clubs": mock_clubs_list})

mock_competitions_json = json.dumps({"competitions": mock_competitions_list})

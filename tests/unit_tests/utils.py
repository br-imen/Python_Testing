
import json


# Mock data for clubs and competitions
mock_clubs_list = [
    {"name": "Club 1", "email": "club1@example.com"},
    {"name": "Club 2", "email": "club2@example.com"}
]

mock_competitions_list = [
    {"name": "Competition 1", "numberOfPlaces": "25"},
    {"name": "Competition 2", "numberOfPlaces": "15"}
]

# Mock data for clubs.json and competitions.json
mock_clubs_json = json.dumps({
    "clubs": mock_clubs_list
})

mock_competitions_json = json.dumps({
    "competitions": mock_competitions_list
})

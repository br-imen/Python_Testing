import json
import pytest
from unittest.mock import mock_open, patch

# Mock data for clubs.json and competitions.json
mock_clubs_json = json.dumps({
    "clubs": [
        {"name": "Club 1", "email": "club1@example.com", "points": "10"},
        {"name": "Club 2", "email": "club2@example.com", "points": "15"}
    ]
})

mock_competitions_json = json.dumps({
    "competitions": [
        {"name": "Competition 1", "date": "2023-03-27 10:00:00",
         "numberOfPlaces": "25"},
        {"name": "Competition 2", "date": "2023-10-22 13:30:00",
         "numberOfPlaces": "15"}
    ]
})


def mocked_open(file, *args, **kwargs):
    """
    Mock open function to return mock data for
    clubs.json and competitions.json
    """
    if file == "clubs.json":
        return mock_open(read_data=mock_clubs_json)()
    elif file == "competitions.json":
        return mock_open(read_data=mock_competitions_json)()
    else:
        raise FileNotFoundError(f"File {file} not found")


# Patch open before importing the app to ensure clubs
# and competitions are loaded with mock data
with patch("builtins.open", side_effect=mocked_open):
    from server import app  # Import app after patching


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

import builtins
import json
import os
import tempfile
import pytest
from unittest.mock import mock_open, patch


clubs_list = [
    {"name": "Club 1", "email": "club1@example.com", "points": "10"},
    {"name": "Club 2", "email": "club2@example.com", "points": "15"},
]

competitions_list = [
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
mock_clubs_json = json.dumps({"clubs": clubs_list})

mock_competitions_json = json.dumps({"competitions": competitions_list})


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
        return builtins.open(file, *args, **kwargs)


# Patch open before importing the app to ensure clubs
# and competitions are loaded with mock data
with patch("builtins.open", side_effect=mocked_open):
    from server import app  # noqa


@pytest.fixture
def temp_clubs_file():
    """
    Create a temporary directory and file for clubs.json
    """
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_club_file_path = os.path.join(temp_dir, "clubs.json")

        # Create a temporary clubs.json file
        clubs_data = {
            "clubs": clubs_list,
        }

        with open(temp_club_file_path, "w") as f:
            json.dump(clubs_data, f, indent=4)

        # Yield the path to the file for the tests
        yield temp_club_file_path


@pytest.fixture
def client(temp_clubs_file):
    """
    Set up the Flask test client and override the CLUB_FILE config
    with the temporary file.
    """
    app.config["TESTING"] = True
    app.config[
        "CLUB_FILE"
    ] = temp_clubs_file  # Override with temp clubs.json path

    with app.test_client() as client:
        yield client

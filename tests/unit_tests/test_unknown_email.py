import json
from unittest.mock import mock_open, patch

from server import get_club_from_email, loadClubs, loadCompetitions
from .utils import (
    mock_clubs_list,
    mock_competitions_list,
    mock_clubs_json,
    mock_competitions_json,
)


# Test for loadClubs function
@patch("builtins.open", new_callable=mock_open, read_data=mock_clubs_json)
@patch("server.json.load")
def test_loadClubs(mock_json_load, mock_file):
    # Mock json.load to return the parsed data
    mock_json_load.return_value = json.loads(mock_clubs_json)

    # Call loadClubs and check if it returns the correct data
    clubs = loadClubs()
    assert len(clubs) == 2
    assert clubs[0]["name"] == "Club 1"
    assert clubs[1]["email"] == "club2@example.com"


# Test for loadCompetitions function
@patch(
    "builtins.open", new_callable=mock_open, read_data=mock_competitions_json
)
@patch("server.json.load")
def test_loadCompetitions(mock_json_load, mock_file):
    # Mock json.load to return the parsed data
    mock_json_load.return_value = json.loads(mock_competitions_json)

    # Call loadCompetitions and check if it returns the correct data
    competitions = loadCompetitions()
    assert len(competitions) == 2
    assert competitions[0]["name"] == "Competition 1"
    assert competitions[1]["numberOfPlaces"] == "15"


@patch("server.clubs", mock_clubs_list)
def test_get_club_from_email_valid():
    club = get_club_from_email("club1@example.com")
    assert club is not None
    assert club["name"] == "Club 1"


@patch("server.clubs", mock_clubs_list)
def test_get_club_from_email_invalid():
    club = get_club_from_email("invalid@example.com")
    assert club is None


# Unit test for showSummary with valid email
@patch(
    "server.competitions", mock_competitions_list
)  # Directly patch the value of competitions
@patch("server.get_club_from_email")
@patch("server.render_template")
def test_showSummary_valid_email(mock_render_template, mock_get_club, client):
    # Mock get_club_from_email to return a valid club
    mock_get_club.return_value = mock_clubs_list[0]

    # Simulate POST request with a valid email
    response = client.post("/showSummary", data={"email": "club1@example.com"})

    # Check if render_template was called with the correct arguments
    mock_render_template.assert_called_once_with(
        "welcome.html",
        club=mock_clubs_list[0],
        competitions=mock_competitions_list,
    )
    assert response.status_code == 200


# Unit test for showSummary with invalid email
@patch("server.get_club_from_email")
@patch("server.flash")
@patch("server.redirect")
@patch("server.url_for")
def test_showSummary_invalid_email(
    mock_url_for, mock_redirect, mock_flash, mock_get_club, client
):
    # Mock get_club_from_email to return None (simulating an invalid email)
    mock_get_club.return_value = None

    # Mock url_for to return a URL for the index page
    mock_url_for.return_value = "/"

    # Simulate POST request with an invalid email
    client.post(
        "/showSummary", data={"email": "invalid@example.com"}
    )

    # Check if flash was called with the correct message
    mock_flash.assert_called_once_with("Sorry, that email wasn't found.")

    # Check if redirect was called with the correct arguments
    mock_redirect.assert_called_once_with("/")

from unittest.mock import patch
from datetime import datetime

from server import validate_competition_date
from .utils import mock_competitions_list, mock_clubs_list

mock_competition_past = {
    "name": "Competition 2",
    "date": "2020-03-27 10:00:00",
    "numberOfPlaces": "15",
}
mock_future_competition = {
    "name": "Future Competition",
    "date": "2024-03-27 10:00:00",
}


# Test for a valid future competition date
@patch("server.datetime")
def test_validate_competition_date_future(mock_datetime):
    # Mock datetime.now() to return a date before the competition date
    mock_datetime.now.return_value = datetime(2023, 3, 27)
    mock_datetime.strptime.side_effect = datetime.strptime

    # Call the function with a future competition
    result = validate_competition_date(mock_future_competition)

    # Assert that no error message is returned
    assert result is None


# Test for a past competition date
@patch("server.datetime")
def test_validate_competition_date_past(mock_datetime):
    # Mock datetime.now() to return a date after the competition date
    mock_datetime.now.return_value = datetime(2023, 3, 27)
    mock_datetime.strptime.side_effect = datetime.strptime

    # Call the function with a past competition
    result = validate_competition_date(mock_competition_past)

    # Assert that the correct error message is returned
    assert (
        result == "This competition is already over. You cannot book a place."
    )


# Test for valid club and valid competition (future date)
@patch("server.render_template")
@patch("server.validate_competition_date")
@patch("server.get_club_from_name")
@patch("server.get_competition_from_name")
def test_book_valid_competition(
    mock_get_competition,
    mock_get_club,
    mock_validate_date,
    mock_render_template,
    client,
):
    # Mock valid club and competition
    mock_get_competition.return_value = mock_competitions_list[0]
    mock_get_club.return_value = mock_clubs_list[0]
    mock_validate_date.return_value = None  # No validation error

    # Simulate GET request to the route
    response = client.get("/book/Competition%201/Club%201")

    # Assert that the necessary functions are called with the correct parameters
    mock_get_competition.assert_called_once_with("Competition 1")
    mock_get_club.assert_called_once_with("Club 1")
    mock_validate_date.assert_called_once_with(mock_competitions_list[0])
    mock_render_template.assert_called_once_with(
        "booking.html",
        club=mock_clubs_list[0],
        competition=mock_competitions_list[0],
    )

    # Check the response status code
    assert response.status_code == 200


# Test for valid club and past competition (competition already over)
@patch("server.competitions", mock_competitions_list)
@patch("server.render_template")
@patch("server.flash")
@patch("server.get_club_from_name")
@patch("server.get_competition_from_name")
@patch("server.validate_competition_date")
def test_book_past_competition(
    mock_validate_date,
    mock_get_competition,
    mock_get_club,
    mock_flash,
    mock_render_template,
    client,
):
    # Mock valid club but past competition
    mock_get_competition.return_value = mock_competition_past
    mock_get_club.return_value = mock_clubs_list[0]
    mock_validate_date.return_value = (
        "This competition is already over. You cannot book a place."
    )

    # Simulate GET request to the route
    response = client.get("/book/Competition%202/Club%201")

    # Assert that the necessary functions are called with the correct parameters
    mock_get_competition.assert_called_once_with("Competition 2")
    mock_get_club.assert_called_once_with("Club 1")
    mock_validate_date.assert_called_once_with(mock_competition_past)
    mock_flash.assert_called_once_with(
        "This competition is already over. You cannot book a place."
    )
    mock_render_template.assert_called_once_with(
        "welcome.html",
        club=mock_clubs_list[0],
        competitions=mock_competitions_list,
    )

    # Check the response status code
    assert response.status_code == 200


# Test for missing club or competition
@patch("server.competitions", mock_competitions_list)
@patch("server.render_template")
@patch("server.flash")
@patch("server.get_club_from_name")
@patch("server.get_competition_from_name")
def test_book_missing_club_or_competition(
    mock_get_competition,
    mock_get_club,
    mock_flash,
    mock_render_template,
    client,
):
    # Mock a case where the competition is missing
    mock_get_competition.return_value = None  # Competition not found
    mock_get_club.return_value = mock_clubs_list[0]  # Club found

    # Simulate GET request to the route
    response = client.get("/book/Competition%201/Club%201")

    # Assert that the necessary functions are called with the correct parameters
    mock_get_competition.assert_called_once_with("Competition 1")
    mock_get_club.assert_called_once_with("Club 1")
    mock_flash.assert_called_once_with("Something went wrong-please try again")
    mock_render_template.assert_called_once_with(
        "welcome.html",
        club=mock_clubs_list[0]["name"],
        competitions=mock_competitions_list,
    )

    # Check the response status code
    assert response.status_code == 200


# Test for invalid club
@patch("server.competitions", mock_competitions_list)
@patch("server.render_template")
@patch("server.flash")
@patch("server.get_club_from_name")
@patch("server.get_competition_from_name")
def test_book_invalid_club(
    mock_get_competition,
    mock_get_club,
    mock_flash,
    mock_render_template,
    client,
):
    # Mock a case where the club is invalid
    mock_get_competition.return_value = mock_competitions_list[
        0
    ]  # Competition found
    mock_get_club.return_value = None  # Club not found

    # Simulate GET request to the route
    response = client.get("/book/Competition%201/Invalid%20Club")

    # Assert that the necessary functions are called with the correct parameters
    mock_get_competition.assert_called_once_with("Competition 1")
    mock_get_club.assert_called_once_with("Invalid Club")
    mock_flash.assert_called_once_with("Something went wrong-please try again")
    mock_render_template.assert_called_once_with(
        "welcome.html", club="Invalid Club", competitions=mock_competitions_list
    )

    # Check the response status code
    assert response.status_code == 200

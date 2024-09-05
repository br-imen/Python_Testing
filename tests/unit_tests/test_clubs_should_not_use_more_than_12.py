from unittest.mock import patch
from .utils import mock_clubs_list, mock_competitions_list


def test_check_places_invalid_more_than_12():
    from server import check_places

    error = check_places("13", mock_clubs_list[0])
    assert error == ("Places required must be a positive"
                     " integer that does not exceed 12")


# Unit test for booking with error in places
@patch("server.redirect")
@patch("server.url_for")
@patch("server.flash")
@patch("server.check_places")
@patch("server.get_club_from_name")
@patch("server.get_competition_from_name")
def test_purchase_places_invalid_places(
    mock_get_competition,
    mock_get_club,
    mock_check_places,
    mock_flash,
    mock_url_for,
    mock_redirect,
    client,
):
    # Mock the functions to simulate an error in places
    mock_get_competition.return_value = mock_competitions_list[0]
    mock_get_club.return_value = mock_clubs_list[0]
    mock_check_places.return_value = (
        "Places required must be a positive integer that does not exceed 12"
    )

    # Mock the redirect and url_for to return a redirect response
    mock_url_for.return_value = "/book"

    # Simulate POST request to the route
    client.post(
        "/purchasePlaces",
        data={"competition": "Competition 1", "club": "Club 1", "places": "20"},
    )

    # Assert that the necessary functions are called with the correct parameters
    mock_get_competition.assert_called_once_with("Competition 1")
    mock_get_club.assert_called_once_with("Club 1")
    mock_check_places.assert_called_once_with("20", mock_clubs_list[0])
    mock_flash.assert_called_once_with(
        "Places required must be a positive integer that does not exceed 12"
    )
    mock_url_for.assert_called_once_with(
        "book",
        competition=mock_competitions_list[0]["name"],
        club=mock_clubs_list[0]["name"],
    )
    mock_redirect.assert_called_once_with("/book")

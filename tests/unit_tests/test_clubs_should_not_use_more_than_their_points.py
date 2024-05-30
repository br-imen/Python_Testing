from unittest.mock import patch
from .utils import mock_clubs_list, mock_competitions_list


# Unit Tests for get_competition_from_name
@patch("server.competitions", mock_competitions_list)
def test_get_competition_from_name_valid():
    from server import get_competition_from_name

    competition = get_competition_from_name("Competition 1")
    assert competition is not None
    assert competition["name"] == "Competition 1"


@patch("server.competitions", mock_competitions_list)
def test_get_competition_from_name_invalid():
    from server import get_competition_from_name

    competition = get_competition_from_name("Invalid Competition")
    assert competition is None


# Unit Tests for get_club_from_name ###
@patch("server.clubs", mock_clubs_list)
def test_get_club_from_name_valid():
    from server import get_club_from_name

    club = get_club_from_name("Club 1")
    assert club is not None
    assert club["name"] == "Club 1"


@patch("server.clubs", mock_clubs_list)
def test_get_club_from_name_invalid():
    from server import get_club_from_name

    club = get_club_from_name("Invalid Club")
    assert club is None


# Unit Tests for check_places ###
def test_check_places_valid():
    from server import check_places

    error = check_places("5", mock_clubs_list[0])
    assert error is None


def test_check_places_invalid_zero():
    from server import check_places

    error = check_places("0", mock_clubs_list[0])
    assert error == "Places required must be a positive integer"


def test_check_places_invalid_negative():
    from server import check_places

    error = check_places("-3", mock_clubs_list[0])
    assert error == "Places required must be a positive integer"


def test_check_places_exceeds_points():
    from server import check_places

    error = check_places("20", mock_clubs_list[0])
    assert error == "Places required exceed club's total points"


# Unit Tests for take_places ###
def test_take_places_valid():
    from server import take_places

    result = take_places(5, mock_clubs_list[0], mock_competitions_list[0])
    assert result is True
    assert mock_clubs_list[0]["points"] == 5  # 10 - 5
    assert mock_competitions_list[0]["numberOfPlaces"] == 20  # 25 - 5


def test_take_places_invalid():
    from server import take_places

    result = take_places(
        "invalid", mock_clubs_list[0], mock_competitions_list[0]
    )
    assert result is False


# Unit test for valid booking
@patch("server.competitions", mock_competitions_list)
@patch("server.render_template")
@patch("server.take_places")
@patch("server.check_places")
@patch("server.get_club_from_name")
@patch("server.get_competition_from_name")
@patch("server.flash")
def test_purchase_places_valid(
    mock_flash,
    mock_get_competition,
    mock_get_club,
    mock_check_places,
    mock_take_places,
    mock_render_template,
    client,
):
    # Mock the functions to return valid data
    mock_get_competition.return_value = mock_competitions_list[0]
    mock_get_club.return_value = mock_clubs_list[0]
    mock_check_places.return_value = None  # No error message
    mock_take_places.return_value = True  # Simulate successful booking

    # Simulate POST request to the route
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Competition 1", "club": "Club 1", "places": "5"},
    )

    # Assert that the necessary functions are called with the correct parameters
    mock_get_competition.assert_called_once_with("Competition 1")
    mock_get_club.assert_called_once_with("Club 1")
    mock_check_places.assert_called_once_with("5", mock_clubs_list[0])
    mock_take_places.assert_called_once_with(
        5, mock_clubs_list[0], mock_competitions_list[0]
    )
    mock_flash.assert_called_once_with("Great-booking complete!")
    mock_render_template.assert_called_once_with(
        "welcome.html",
        club=mock_clubs_list[0],
        competitions=mock_competitions_list,
    )

    # Check response status code
    assert response.status_code == 200


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
        "Places required exceed club's total points"
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
        "Places required exceed club's total points"
    )
    mock_url_for.assert_called_once_with(
        "book",
        competition=mock_competitions_list[0]["name"],
        club=mock_clubs_list[0]["name"],
    )
    mock_redirect.assert_called_once_with("/book")


# Unit test for failed booking due to take_places failure
@patch("server.redirect")
@patch("server.url_for")
@patch("server.flash")
@patch("server.take_places")
@patch("server.check_places")
@patch("server.get_club_from_name")
@patch("server.get_competition_from_name")
def test_purchase_places_failed_take_places(
    mock_get_competition,
    mock_get_club,
    mock_check_places,
    mock_take_places,
    mock_flash,
    mock_url_for,
    mock_redirect,
    client,
):
    # Mock the functions to simulate an error in take_places
    mock_get_competition.return_value = mock_competitions_list[0]
    mock_get_club.return_value = mock_clubs_list[0]
    mock_check_places.return_value = None  # No error message
    mock_take_places.return_value = False  # Simulate failure in taking places

    # Mock the redirect and url_for to return a redirect response
    mock_url_for.return_value = "/book"

    # Simulate POST request to the route
    client.post(
        "/purchasePlaces",
        data={"competition": "Competition 1", "club": "Club 1", "places": "5"},
    )

    # Assert that the necessary functions are called with the correct parameters
    mock_get_competition.assert_called_once_with("Competition 1")
    mock_get_club.assert_called_once_with("Club 1")
    mock_check_places.assert_called_once_with("5", mock_clubs_list[0])
    mock_take_places.assert_called_once_with(
        5, mock_clubs_list[0], mock_competitions_list[0]
    )
    mock_flash.assert_called_once_with("Something went wrong-please try again")
    mock_url_for.assert_called_once_with(
        "book",
        competition=mock_competitions_list[0]["name"],
        club=mock_clubs_list[0]["name"],
    )
    mock_redirect.assert_called_once_with("/book")

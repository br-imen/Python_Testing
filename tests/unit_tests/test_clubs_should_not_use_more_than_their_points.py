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

from unittest.mock import mock_open, patch
from server import update_clubs, get_index_club


def test_get_index_club(mock_clubs_fixture):
    # Test finding the index of a club
    with patch("server.clubs", mock_clubs_fixture):
        club = mock_clubs_fixture[0]
        index = get_index_club(club)
    assert index == 0


@patch("builtins.open", new_callable=mock_open)
@patch("json.dump")
def test_update_clubs_success(mock_json_dump, mock_file, mock_clubs_fixture):
    club = {"name": "Club 1", "points": "20"}
    index = 0
    with patch("server.clubs", mock_clubs_fixture):
        result = update_clubs(club, index)

    assert result is True
    assert mock_clubs_fixture[0]["points"] == "20"
    mock_json_dump.assert_called_once()
    mock_file.assert_called_once()


@patch("builtins.open", side_effect=FileNotFoundError)
def test_update_clubs_file_not_found(mock_file, mock_clubs_fixture):
    # Club to be updated
    club = {"name": "Club 1", "points": "20"}
    index = 0

    # Test update_clubs when FileNotFoundError is raised
    with patch("server.clubs", mock_clubs_fixture):
        result = update_clubs(club, index)

    # Assert that the function returns False
    assert result is False

    # Assert that no changes were made to the clubs list
    assert (
        mock_clubs_fixture[0]["points"] == "10"
    )  # The points shouldn't be updated

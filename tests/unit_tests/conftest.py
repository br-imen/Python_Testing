import pytest
from server import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_clubs_fixture():
    return [
        {"name": "Club 1", "email": "club1@example.com", "points": "10"},
        {"name": "Club 2", "email": "club2@example.com", "points": "15"},
    ]

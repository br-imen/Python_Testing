def test_book_valid_competition(client):
    """
    Test booking a valid competition with a valid club
    (future competition date).
    """
    response = client.get("/book/Competition%201/Club%201")

    # Ensure the correct template is rendered (booking.html)
    assert response.status_code == 200
    assert (
        b"Competition 1" in response.data
    )  # Assuming the booking page has the word "Booking"


def test_book_past_competition(client):
    """
    Test booking a competition with a past date.
    """
    response = client.get("/book/Competition%202/Club%201")

    # Ensure the user is shown a message that the competition is in the past
    assert response.status_code == 200
    assert (
        b"This competition is already over. You cannot book a place."
        in response.data
    )


def test_book_invalid_competition(client):
    """
    Test trying to book with an invalid competition name.
    """
    response = client.get("/book/Invalid%20Competition/Club%201")

    # Ensure the correct message is shown when competition is invalid
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data


def test_book_invalid_club(client):
    """
    Test trying to book with an invalid club name.
    """
    response = client.get("/book/Competition%201/Invalid%20Club")

    # Ensure the correct message is shown when club is invalid
    assert response.status_code == 200
    assert b"Something went wrong-please try again" in response.data

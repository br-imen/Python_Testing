
# Integration test for valid email
def test_showSummary_valid_email_integration(client):
    # Simulate POST request with a valid email
    response = client.post("/showSummary", data={"email": "club1@example.com"})

    # Check if the welcome page is rendered with the correct club data
    assert response.status_code == 200
    assert b"Welcome" in response.data


# Integration test for invalid email
def test_showSummary_invalid_email_integration(client):
    # Simulate POST request with an invalid email
    response = client.post(
        "/showSummary", data={"email": "invalid@example.com"}
    )

    # Validate that the response redirects to the index page
    assert response.status_code == 302
    response = client.get(response.headers["Location"])  # Follow the redirect

    # Check if the flash message appears in the redirected page
    assert b"Sorry, that email wasn&#39;t found." in response.data

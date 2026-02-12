import pytest
import requests
import re
from config import BASE_URL
from config import HEADERS

def test_page_2_users(get_users):
    response = get_users
    
    # Verify the request was successful
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"

    # Parse the response body
    response_body = response.json()

    # Assert existence of "total"
    assert "total" in response_body, "Field 'total' not found in response"
    received_total = response_body["total"]

    # Get the list of users from "data"
    users_data = response_body["data"]
    
    # Make sure that at least 2 users exists
    assert len(users_data) >= 2, "Less than 2 users returned in 'data'"

    # Assert "last_name" for the first two Users
    assert "last_name" in users_data[0], "First user missing 'last_name'"
    assert "last_name" in users_data[1], "Second user missing 'last_name'"

    # Count number of users in "data" and compare to "total"
    users_count = len(users_data)
    assert users_count <= received_total, f"Page count ({users_count}) exceeds Total ({received_total})"
    
def test_response_data_types(get_users):
    response = get_users
    response_body = response.json()
    # Assert Metadata Types
    assert isinstance(response_body["page"], int)
    assert isinstance(response_body["per_page"], int)
    assert isinstance(response_body["total"], int)
    assert isinstance(response_body["total_pages"], int)
    assert isinstance(response_body["data"], list)

    # Assert Data Object Types (Inside the 'data' list)
    for user in response_body["data"]:
        assert isinstance(user["id"], int)
        assert isinstance(user["email"], str)
        assert isinstance(user["first_name"], str)
        assert isinstance(user["last_name"], str)
        assert isinstance(user["avatar"], str)
        
        # Specific Format Assertions
        regex_email = r"^[a-zA-Z0-9.!#$%&'*+\/=?^_`{|}~-]+@[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$"
        # Assert email correct format
        assert re.fullmatch(regex_email, user["email"]), f"Email {user['email']} does not match the required format"
        assert user["avatar"].startswith("https://"), "Avatar should be a valid URL"

# Fixture to get data about users 
@pytest.fixture(scope="module")
def get_users():
    # Send a proper Request
    url = f"{BASE_URL}/api/users?page=2"
    response_get = requests.get(url, headers = HEADERS)
    return response_get
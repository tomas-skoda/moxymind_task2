import pytest
import requests
from config import BASE_URL
from config import HEADERS
from jsonschema import validate
import json

# --- External Data Source ---
# This could be moved to a separate .json or .csv file


#@pytest.mark.parametrize("user_info", create_users)
def test_create_user(create_users):
    time_limit_ms = 1000  # Set response time limit as variable
    for response_body in create_users:
        #Assert HTTP Code (201 Created)
        assert response_body.status_code == 201
        
        user_data = response_body.json()
        
        #Assert ID exists
        assert "id" in user_data
        
        #Assert Timestamp of createdAt
        assert "createdAt" in user_data

        # 5. Assert Response time < limit
        # response.elapsed.total_seconds() returns seconds; multiply by 1000 for ms
        actual_response_time = response_body.elapsed.total_seconds() * 1000
        assert actual_response_time < time_limit_ms, f"Response too slow: {actual_response_time}ms"
        print(f"\nUser {user_data['name']} created in {actual_response_time:.2f}ms")

def test_reponse_schema(create_users):
    # User scheme expected from the API
    USER_SCHEMA = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "job": {"type": "string"},
            "id": {
                "type": "string",
                # Chekc if ID is number
                "pattern": r"^\d+$"
            },
            "createdAt": {
                "type": "string",
                # Verify it matches an ISO 8601-like format (e.g., 2026-02-10T12:42:48.000Z)
                "pattern": r"^\d{4}-[01]\d-[0-3]\dT[0-2]\d(?::[0-5]\d){2}\.\d+Z$" 
            }
        },
        "required": ["name", "job", "id", "createdAt"],
        # Must be True because reqres.in _meta data. In real tests tadditionalProperties would be False
        "additionalProperties": True 
    }

    # This will raise a ValidationError if the response doesn't match the schema
    for response_body in create_users:
        user_data = response_body.json()
        validate(instance = user_data, schema = USER_SCHEMA)

# Helper function to load data
def load_test_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

#Fixture to create users from external data 
@pytest.fixture(scope="module")
def create_users():
    url = f"{BASE_URL}/api/users"
    users_data = load_test_data("external_users_data.json")
    responses = []
    #Send a proper Request
    for user_data in users_data:
        response_post = requests.post(url, headers = HEADERS, json = user_data)
        responses.append(response_post)
    return responses

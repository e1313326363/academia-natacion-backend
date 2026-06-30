import requests

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = "/api/login"
TIMEOUT = 30

def test_post_api_login_with_valid_credentials():
    url = BASE_URL + LOGIN_ENDPOINT
    payload = {
        "email": "admin@academia.com",
        "password": "admin123"
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 200, f"Expected status 200 but got {response.status_code}"
    
    try:
        json_response = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Validate keys in response
    assert "token" in json_response, "Response JSON missing 'token' field"
    assert isinstance(json_response["token"], str) and json_response["token"], "'token' field is not a non-empty string"
    assert "user" in json_response, "Response JSON missing 'user' field"
    user = json_response["user"]
    expected_user_fields = ["id", "name", "email", "role"]
    for field in expected_user_fields:
        assert field in user, f"User object missing '{field}' field"
        assert user[field] is not None, f"User field '{field}' is None"

test_post_api_login_with_valid_credentials()
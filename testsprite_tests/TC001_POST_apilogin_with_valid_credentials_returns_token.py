import requests

BASE_URL = "http://localhost:8000"

def test_post_api_login_with_valid_credentials_returns_token():
    url = f"{BASE_URL}/api/login"
    payload = {
        "email": "admin@academia.com",
        "password": "admin123"
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    try:
        json_data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert "token" in json_data, "Response JSON missing 'token'"
    assert isinstance(json_data["token"], str) and json_data["token"], "'token' should be a non-empty string"

    assert "user" in json_data, "Response JSON missing 'user'"
    user = json_data["user"]
    assert isinstance(user, dict), "'user' should be an object"
    for key in ("id", "name", "email", "role"):
        assert key in user, f"'user' object missing '{key}' key"
    assert isinstance(user["id"], int), "'user.id' should be int"
    assert isinstance(user["name"], str) and user["name"], "'user.name' should be non-empty string"
    assert isinstance(user["email"], str) and user["email"], "'user.email' should be non-empty string"
    assert isinstance(user["role"], str) and user["role"], "'user.role' should be non-empty string"


test_post_api_login_with_valid_credentials_returns_token()
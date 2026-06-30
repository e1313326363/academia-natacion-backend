import requests

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{BASE_URL}/api/login"
ESTUDIANTES_ENDPOINT = f"{BASE_URL}/api/estudiantes"
TIMEOUT = 30

def test_get_estudiantes_returns_paginated_list():
    # First, authenticate to get Bearer token
    login_payload = {
        "email": "admin@academia.com",
        "password": "admin123"
    }
    try:
        login_response = requests.post(LOGIN_ENDPOINT, json=login_payload, timeout=TIMEOUT)
        assert login_response.status_code == 200, f"Login failed with status {login_response.status_code}"
        login_json = login_response.json()
        token = login_json.get("token")
        assert token and isinstance(token, str), "Token missing or not string in login response"
    except requests.RequestException as e:
        assert False, f"Login request exception: {e}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Call GET /api/estudiantes without filters (default pagination)
    try:
        response = requests.get(ESTUDIANTES_ENDPOINT, headers=headers, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request to GET /api/estudiantes failed: {e}"

    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Validate paginated response fields
    # Should contain: data (array), total (int), current_page (int), last_page (int)
    assert isinstance(data, dict), "Response JSON is not an object"
    assert "data" in data, "Response missing 'data' field"
    assert isinstance(data["data"], list), "'data' field is not a list"
    for item in data["data"]:
        assert isinstance(item, dict), "Items in 'data' array must be objects"

    assert "total" in data, "Response missing 'total' field"
    assert isinstance(data["total"], int), "'total' field is not an integer"

    assert "current_page" in data, "Response missing 'current_page' field"
    assert isinstance(data["current_page"], int), "'current_page' field is not an integer"

    assert "last_page" in data, "Response missing 'last_page' field"
    assert isinstance(data["last_page"], int), "'last_page' field is not an integer"

test_get_estudiantes_returns_paginated_list()
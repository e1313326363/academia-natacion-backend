import requests

BASE_URL = "http://localhost:8000"
LOGIN_EMAIL = "admin@academia.com"
LOGIN_PASSWORD = "admin123"
TIMEOUT = 30

def test_get_instructores_returns_paginated_list():
    # Authenticate and get Bearer token
    login_url = f"{BASE_URL}/api/login"
    login_payload = {
        "email": LOGIN_EMAIL,
        "password": LOGIN_PASSWORD
    }
    login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    login_data = login_resp.json()
    token = login_data.get("token")
    assert token and isinstance(token, str), "Token not found in login response"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Call GET /api/instructores
    instructores_url = f"{BASE_URL}/api/instructores"
    params = {
        "page": 1
    }
    resp = requests.get(instructores_url, headers=headers, params=params, timeout=TIMEOUT)
    assert resp.status_code == 200, f"Failed to get instructores: {resp.status_code} {resp.text}"

    json_data = resp.json()

    # Validate paginated structure: expect keys like data (list), total, current_page, last_page
    assert isinstance(json_data, dict), "Response is not a JSON object"
    assert "data" in json_data and isinstance(json_data["data"], list), "'data' key missing or not a list"
    assert "total" in json_data and isinstance(json_data["total"], int), "'total' key missing or not int"
    assert "current_page" in json_data and isinstance(json_data["current_page"], int), "'current_page' missing or not int"
    assert "last_page" in json_data and isinstance(json_data["last_page"], int), "'last_page' missing or not int"

    # Check each instructor in data has nombre and especialidad fields (especialidad can be None)
    for instructor in json_data["data"]:
        assert isinstance(instructor, dict), "Instructor item is not an object"
        assert "nombre" in instructor and isinstance(instructor["nombre"], str), "Instructor missing 'nombre' or not string"
        # especialidad is optional but should be present (including None or string)
        assert "especialidad" in instructor, "'especialidad' key missing in instructor"
        assert (instructor["especialidad"] is None) or isinstance(instructor["especialidad"], str), "'especialidad' should be string or None"

test_get_instructores_returns_paginated_list()
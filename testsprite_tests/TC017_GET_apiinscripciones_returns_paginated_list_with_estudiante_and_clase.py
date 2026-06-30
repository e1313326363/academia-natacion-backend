import requests
import pytest

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = "/api/login"
INSCRIPCIONES_ENDPOINT = "/api/inscripciones"

USER_EMAIL = "admin@academia.com"
USER_PASSWORD = "admin123"

TIMEOUT = 30


def get_auth_token():
    login_url = BASE_URL + LOGIN_ENDPOINT
    payload = {"email": USER_EMAIL, "password": USER_PASSWORD}
    response = requests.post(login_url, json=payload, timeout=TIMEOUT)
    assert response.status_code == 200, f"Login failed with status {response.status_code}"
    data = response.json()
    assert "token" in data, "No token in login response"
    return data["token"]


def test_get_inscripciones_returns_paginated_list_with_estudiante_and_clase():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}

    params = {"page": 1}  # Query page 1, can be adjusted if needed
    response = requests.get(BASE_URL + INSCRIPCIONES_ENDPOINT, headers=headers, params=params, timeout=TIMEOUT)
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"
    data = response.json()

    # Validate paginated structure keys presence
    assert isinstance(data, dict), "Response is not a JSON object"
    assert "data" in data, "Response JSON missing 'data' key"
    assert "current_page" in data, "Response JSON missing 'current_page' key"
    assert "last_page" in data, "Response JSON missing 'last_page' key"
    assert "per_page" in data, "Response JSON missing 'per_page' key"
    assert "total" in data, "Response JSON missing 'total' key"

    # Validate data array is list
    enrollments = data["data"]
    assert isinstance(enrollments, list), "'data' is not a list"

    if len(enrollments) > 0:
        enrollment = enrollments[0]

        # Each enrollment should have estudiante and clase nested objects
        assert "estudiante" in enrollment, "Enrollment missing 'estudiante' key"
        assert isinstance(enrollment["estudiante"], dict), "'estudiante' is not an object"
        assert "id" in enrollment["estudiante"], "'estudiante' missing 'id'"
        assert "nombre" in enrollment["estudiante"] or "name" in enrollment["estudiante"], "'estudiante' missing 'nombre' or 'name'"

        assert "clase" in enrollment, "Enrollment missing 'clase' key"
        assert isinstance(enrollment["clase"], dict), "'clase' is not an object"
        assert "id" in enrollment["clase"], "'clase' missing 'id'"
        assert "nombre_clase" in enrollment["clase"] or "nombre" in enrollment["clase"], "'clase' missing 'nombre_clase' or 'nombre'"
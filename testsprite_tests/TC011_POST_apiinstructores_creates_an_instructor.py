import requests

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{BASE_URL}/api/login"
INSTRUCTORES_ENDPOINT = f"{BASE_URL}/api/instructores"


def test_post_api_instructores_creates_instructor():
    # Credentials assumed known from PRD for admin user
    login_payload = {
        "email": "admin@academia.com",
        "password": "admin123"
    }
    timeout = 30

    # Authenticate first to get Bearer token
    login_resp = requests.post(LOGIN_ENDPOINT, json=login_payload, timeout=timeout)
    assert login_resp.status_code == 200, f"Login failed with status {login_resp.status_code}"
    login_data = login_resp.json()
    token = login_data.get("token")
    assert token and isinstance(token, str), "Token missing or invalid in login response"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    instructor_payload = {
        "nombre": "Test Instructor Nombre"
    }

    # Create new instructor via POST /api/instructores
    post_resp = requests.post(INSTRUCTORES_ENDPOINT, json=instructor_payload, headers=headers, timeout=timeout)
    try:
        assert post_resp.status_code == 201, f"Expected status 201, got {post_resp.status_code}"
        data = post_resp.json()
        # Validate the response contains at least 'id' and 'nombre' with correct value
        assert "id" in data and isinstance(data["id"], int), "Response missing valid 'id'"
        assert data.get("nombre") == instructor_payload["nombre"], "Response 'nombre' does not match request"
    finally:
        # Cleanup: delete the created instructor
        if post_resp.status_code == 201:
            instructor_id = post_resp.json().get("id")
            if instructor_id:
                del_resp = requests.delete(f"{INSTRUCTORES_ENDPOINT}/{instructor_id}", headers=headers, timeout=timeout)
                assert del_resp.status_code == 200, f"Cleanup failed, DELETE status {del_resp.status_code}"


test_post_api_instructores_creates_instructor()
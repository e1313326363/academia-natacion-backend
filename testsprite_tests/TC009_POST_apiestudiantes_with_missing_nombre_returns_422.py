import requests

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{BASE_URL}/api/login"
ESTUDIANTES_ENDPOINT = f"{BASE_URL}/api/estudiantes"

# Credentials for authentication - assumed valid user with permission
EMAIL = "admin@academia.com"
PASSWORD = "admin123"

def test_post_estudiantes_missing_nombre_returns_422():
    # Authenticate to get Bearer token
    login_payload = {"email": EMAIL, "password": PASSWORD}
    login_response = requests.post(LOGIN_ENDPOINT, json=login_payload, timeout=30)
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    token = login_response.json().get("token")
    assert token, "No token received in login response"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Prepare payload missing 'nombre' field (required)
    payload = {
        "fecha_nacimiento": "2010-01-01",  # valid date but no nombre
        "telefono": "1234567890",
        "email": "example@student.com"
    }

    response = requests.post(ESTUDIANTES_ENDPOINT, json=payload, headers=headers, timeout=30)

    # Assert validation error 422 is returned due to missing nombre
    assert response.status_code == 422, f"Expected 422, got {response.status_code} with body: {response.text}"

test_post_estudiantes_missing_nombre_returns_422()
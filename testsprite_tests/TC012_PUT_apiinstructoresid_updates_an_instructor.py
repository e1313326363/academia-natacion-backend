import requests

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = "/api/login"
INSTRUCTORES_ENDPOINT = "/api/instructores"
TIMEOUT = 30

def test_put_api_instructores_id_updates_instructor():
    # Login to get Bearer token
    login_payload = {
        "email": "admin@academia.com",
        "password": "admin123"
    }
    login_response = requests.post(
        BASE_URL + LOGIN_ENDPOINT,
        json=login_payload,
        timeout=TIMEOUT
    )
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    login_data = login_response.json()
    token = login_data.get("token")
    assert token, "No token in login response"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    # Create a new instructor to update, so we don't depend on existing data
    create_payload = {
        "nombre": "Test Instructor TC012",
        "especialidad": "Natación Básica",
        "email": "tc012_instructor@example.com"
    }
    created_response = requests.post(
        BASE_URL + INSTRUCTORES_ENDPOINT,
        json=create_payload,
        headers=headers,
        timeout=TIMEOUT
    )
    assert created_response.status_code == 201, f"Failed to create instructor: {created_response.text}"
    created_instructor = created_response.json()
    instructor_id = created_instructor.get("id")
    assert instructor_id is not None, "Created instructor has no id"

    try:
        # Prepare update payload for PUT
        update_payload = {
            "nombre": "Updated Instructor TC012",
            "especialidad": "Natación Avanzada"
        }
        put_response = requests.put(
            f"{BASE_URL}{INSTRUCTORES_ENDPOINT}/{instructor_id}",
            json=update_payload,
            headers=headers,
            timeout=TIMEOUT
        )
        assert put_response.status_code == 200, f"PUT update failed: {put_response.text}"
        updated_instructor = put_response.json()
        # Validate the updated fields
        assert updated_instructor.get("id") == instructor_id, "Instructor ID mismatch after update"
        assert updated_instructor.get("nombre") == update_payload["nombre"], "Nombre not updated correctly"
        # especialidad may be optional in response, but we expect the updated value
        assert updated_instructor.get("especialidad") == update_payload["especialidad"], "Especialidad not updated correctly"
    finally:
        # Clean up: delete the created instructor
        del_response = requests.delete(
            f"{BASE_URL}{INSTRUCTORES_ENDPOINT}/{instructor_id}",
            headers=headers,
            timeout=TIMEOUT
        )
        assert del_response.status_code == 200, f"Failed to delete instructor during cleanup: {del_response.text}"

test_put_api_instructores_id_updates_instructor()
import requests
from datetime import date, timedelta
import uuid

BASE_URL = "http://localhost:8000"
LOGIN_EMAIL = "admin@academia.com"
LOGIN_PASSWORD = "admin123"
TIMEOUT = 30

def test_post_api_estudiantes_creates_student():
    # Login to obtain Bearer token
    login_url = f"{BASE_URL}/api/login"
    login_payload = {"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
    login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token = login_resp.json().get("token")
    assert token, "No token received in login response"

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Prepare unique student data
    unique_suffix = uuid.uuid4().hex[:8]
    nombre = f"TestStudent{unique_suffix}"
    fecha_nacimiento = (date.today() - timedelta(days=1)).isoformat()

    estudiantes_url = f"{BASE_URL}/api/estudiantes"

    created_student_id = None
    try:
        # Create a new student
        create_payload = {
            "nombre": nombre,
            "fecha_nacimiento": fecha_nacimiento
        }
        create_resp = requests.post(estudiantes_url, json=create_payload, headers=headers, timeout=TIMEOUT)
        assert create_resp.status_code == 201, f"Expected 201, got {create_resp.status_code}: {create_resp.text}"

        created_student = create_resp.json()
        assert isinstance(created_student, dict), f"Response is not a dict: {created_student}"
        # Validate fields present and matching input
        assert "id" in created_student, "Created student has no 'id'"
        assert created_student.get("nombre") == nombre, f"Nombre mismatch: expected {nombre}, got {created_student.get('nombre')}"
        # fecha_nacimiento may be returned in different date format but should contain the input date
        assert created_student.get("fecha_nacimiento") == fecha_nacimiento, f"fecha_nacimiento mismatch: expected {fecha_nacimiento}, got {created_student.get('fecha_nacimiento')}"

        created_student_id = created_student["id"]
    finally:
        # Cleanup: delete the created student if created
        if created_student_id is not None:
            delete_url = f"{estudiantes_url}/{created_student_id}"
            del_resp = requests.delete(delete_url, headers=headers, timeout=TIMEOUT)
            assert del_resp.status_code == 200, f"Failed to delete student {created_student_id}: {del_resp.text}"

test_post_api_estudiantes_creates_student()

import requests
import datetime

BASE_URL = "http://localhost:8000"
LOGIN_EMAIL = "admin@academia.com"
LOGIN_PASSWORD = "admin123"
TIMEOUT = 30

def login_get_token():
    url = f"{BASE_URL}/api/login"
    payload = {"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
    resp = requests.post(url, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    token = resp.json().get("token")
    assert token, "No token received in login response"
    return token

def create_student(token, nombre, fecha_nacimiento, telefono=None, email=None):
    url = f"{BASE_URL}/api/estudiantes"
    headers = {"Authorization": f"Bearer {token}"}
    data = {"nombre": nombre, "fecha_nacimiento": fecha_nacimiento}
    if telefono:
        data["telefono"] = telefono
    if email:
        data["email"] = email
    resp = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    assert resp.status_code == 201, f"Expected 201 Created, got {resp.status_code}"
    return resp.json()

def delete_student(token, student_id):
    url = f"{BASE_URL}/api/estudiantes/{student_id}"
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(url, headers=headers, timeout=TIMEOUT)
    if resp.status_code != 200 and resp.status_code != 404:
        resp.raise_for_status()

def test_put_api_estudiantes_update_student():
    token = login_get_token()
    headers = {"Authorization": f"Bearer {token}"}
    # Create a new student for testing
    original_nombre = "Test Student"
    original_fecha = "2005-05-15"
    student = create_student(token, original_nombre, original_fecha)
    student_id = student.get("id")
    assert student_id, "Created student has no ID"
    try:
        # Prepare updated data - change nombre only, keep fecha_nacimiento same
        updated_nombre = "Updated Student Name"
        update_data = {
            "nombre": updated_nombre,
            "fecha_nacimiento": original_fecha  # required field
        }
        url = f"{BASE_URL}/api/estudiantes/{student_id}"
        resp = requests.put(url, json=update_data, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
        assert resp.status_code == 200, f"Expected 200 OK, got {resp.status_code}"
        student_updated = resp.json()
        # Validate updated nombre and that fecha_nacimiento remains unchanged
        assert student_updated.get("nombre") == updated_nombre, "Nombre was not updated correctly"
        assert student_updated.get("fecha_nacimiento") == original_fecha, "fecha_nacimiento changed unexpectedly"
        # Optionally check other fields remain or are present
        assert "id" in student_updated and student_updated["id"] == student_id
    finally:
        # Clean up: delete the created student
        delete_student(token, student_id)

test_put_api_estudiantes_update_student()
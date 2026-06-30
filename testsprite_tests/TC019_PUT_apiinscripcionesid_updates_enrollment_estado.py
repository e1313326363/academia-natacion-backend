import requests
import datetime

BASE_URL = "http://localhost:8000"
EMAIL = "admin@academia.com"
PASSWORD = "admin123"
TIMEOUT = 30

def test_put_api_inscripciones_id_updates_estado_suspendido():
    # Authenticate and get token
    login_payload = {"email": EMAIL, "password": PASSWORD}
    login_resp = requests.post(f"{BASE_URL}/api/login", json=login_payload, timeout=TIMEOUT)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token = login_resp.json().get("token")
    assert token, "No token found in login response"
    headers = {"Authorization": f"Bearer {token}"}

    # Helper to create a student
    def create_student():
        today = datetime.date.today()
        student_payload = {
            "nombre": "Test Student TC019",
            "fecha_nacimiento": (today.replace(year=today.year - 20)).isoformat()
        }
        resp = requests.post(f"{BASE_URL}/api/estudiantes", json=student_payload, headers=headers, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Student creation failed: {resp.text}"
        return resp.json()["id"]

    # Helper to create an instructor
    def create_instructor():
        instructor_payload = {
            "nombre": "Test Instructor TC019"
        }
        resp = requests.post(f"{BASE_URL}/api/instructores", json=instructor_payload, headers=headers, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Instructor creation failed: {resp.text}"
        return resp.json()["id"]

    # Helper to create a level (nivel)
    def create_level():
        level_payload = {
            "nombre_nivel": "Nivel TC019"
        }
        resp = requests.post(f"{BASE_URL}/api/niveles", json=level_payload, headers=headers, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Level creation failed: {resp.text}"
        return resp.json()["id"]

    # Helper to create a class
    def create_class(id_nivel, id_instructor):
        class_payload = {
            "nombre_clase": "Clase TC019",
            "id_nivel": id_nivel,
            "id_instructor": id_instructor,
            "cupo": 10
        }
        resp = requests.post(f"{BASE_URL}/api/clases", json=class_payload, headers=headers, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Class creation failed: {resp.text}"
        return resp.json()["id"]

    # Helper to create enrollment
    def create_enrollment(id_estudiante, id_clase):
        enrollment_payload = {
            "id_estudiante": id_estudiante,
            "id_clase": id_clase
        }
        resp = requests.post(f"{BASE_URL}/api/inscripciones", json=enrollment_payload, headers=headers, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Enrollment creation failed: {resp.text}"
        return resp.json()["id"]

    # Helper to delete enrollment
    def delete_enrollment(id_inscripcion):
        resp = requests.delete(f"{BASE_URL}/api/inscripciones/{id_inscripcion}", headers=headers, timeout=TIMEOUT)
        assert resp.status_code == 200, f"Enrollment deletion failed: {resp.text}"

    # Helper to delete class
    def delete_class(id_clase):
        resp = requests.delete(f"{BASE_URL}/api/clases/{id_clase}", headers=headers, timeout=TIMEOUT)
        assert resp.status_code == 200, f"Class deletion failed: {resp.text}"

    # Helper to delete level
    def delete_level(id_nivel):
        resp = requests.delete(f"{BASE_URL}/api/niveles/{id_nivel}", headers=headers, timeout=TIMEOUT)
        assert resp.status_code == 200, f"Level deletion failed: {resp.text}"

    # Helper to delete instructor
    def delete_instructor(id_instructor):
        resp = requests.delete(f"{BASE_URL}/api/instructores/{id_instructor}", headers=headers, timeout=TIMEOUT)
        assert resp.status_code == 200, f"Instructor deletion failed: {resp.text}"

    # Helper to delete student
    def delete_student(id_estudiante):
        resp = requests.delete(f"{BASE_URL}/api/estudiantes/{id_estudiante}", headers=headers, timeout=TIMEOUT)
        assert resp.status_code == 200, f"Student deletion failed: {resp.text}"

    # Create all needed resources and enrollment, then update estado
    id_estudiante = create_student()
    id_instructor = create_instructor()
    id_nivel = create_level()
    id_clase = create_class(id_nivel, id_instructor)
    id_inscripcion = create_enrollment(id_estudiante, id_clase)

    try:
        # Update enrollment estado to Suspendido
        update_payload = {"estado": "Suspendido"}
        update_resp = requests.put(f"{BASE_URL}/api/inscripciones/{id_inscripcion}", json=update_payload, headers=headers, timeout=TIMEOUT)
        assert update_resp.status_code == 200, f"Update enrollment failed: {update_resp.text}"
        updated_enrollment = update_resp.json()
        assert updated_enrollment["estado"] == "Suspendido", f"Estado not updated, got: {updated_enrollment.get('estado')}"

        # Optionally verify GET returns updated status
        get_resp = requests.get(f"{BASE_URL}/api/inscripciones", headers=headers, timeout=TIMEOUT)
        assert get_resp.status_code == 200, f"Get enrollments failed: {get_resp.text}"
        found = False
        for item in get_resp.json().get("data", []):
            if item["id"] == id_inscripcion:
                assert item["estado"] == "Suspendido", f"Enrollment estado in list not updated correctly: {item['estado']}"
                found = True
                break
        assert found, "Updated enrollment not found in enrollment list"

    finally:
        # Cleanup all created resources
        delete_enrollment(id_inscripcion)
        delete_class(id_clase)
        delete_level(id_nivel)
        delete_instructor(id_instructor)
        delete_student(id_estudiante)

test_put_api_inscripciones_id_updates_estado_suspendido()
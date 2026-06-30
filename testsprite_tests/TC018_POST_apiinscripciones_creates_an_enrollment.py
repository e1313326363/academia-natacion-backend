import requests
import datetime

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{BASE_URL}/api/login"
INSCRIPTION_ENDPOINT = f"{BASE_URL}/api/inscripciones"
STUDENTS_ENDPOINT = f"{BASE_URL}/api/estudiantes"
CLASSES_ENDPOINT = f"{BASE_URL}/api/clases"

ADMIN_EMAIL = "admin@academia.com"
ADMIN_PASSWORD = "admin123"
TIMEOUT = 30

def login():
    payload = {"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD}
    resp = requests.post(LOGIN_ENDPOINT, json=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    token = resp.json().get("token")
    assert token and isinstance(token, str)
    return token

def create_student(token):
    headers = {"Authorization": f"Bearer {token}"}
    today = datetime.date.today()
    birth_date = today.replace(year=today.year - 10).isoformat()
    payload = {
        "nombre": "Test Student TC018",
        "fecha_nacimiento": birth_date
    }
    response = requests.post(STUDENTS_ENDPOINT, json=payload, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    assert response.status_code == 201
    student = response.json()
    assert "id" in student and isinstance(student["id"], int)
    return student["id"]

def delete_student(token, student_id):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(f"{STUDENTS_ENDPOINT}/{student_id}", headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    assert resp.status_code == 200

def create_instructor(token):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"nombre": "Test Instructor TC018"}
    resp = requests.post(f"{BASE_URL}/api/instructores", json=payload, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    assert resp.status_code == 201
    instructor = resp.json()
    assert "id" in instructor and isinstance(instructor["id"], int)
    return instructor["id"]

def delete_instructor(token, instructor_id):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(f"{BASE_URL}/api/instructores/{instructor_id}", headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    assert resp.status_code == 200

def create_level(token):
    headers = {"Authorization": f"Bearer {token}"}
    unique_name = f"Nivel Test TC018 {datetime.datetime.utcnow().timestamp()}"
    payload = {"nombre_nivel": unique_name}
    resp = requests.post(f"{BASE_URL}/api/niveles", json=payload, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    assert resp.status_code == 201
    level = resp.json()
    assert "id" in level and isinstance(level["id"], int)
    return level["id"]

def delete_level(token, level_id):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(f"{BASE_URL}/api/niveles/{level_id}", headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    assert resp.status_code == 200

def create_class(token, nivel_id, instructor_id):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "nombre_clase": "Test Class TC018",
        "id_nivel": nivel_id,
        "id_instructor": instructor_id,
        "cupo": 10
    }
    resp = requests.post(CLASSES_ENDPOINT, json=payload, headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    assert resp.status_code == 201
    clase = resp.json()
    assert "id" in clase and isinstance(clase["id"], int)
    return clase["id"]

def delete_class(token, class_id):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(f"{CLASSES_ENDPOINT}/{class_id}", headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    assert resp.status_code == 200

def delete_enrollment(token, enrollment_id):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(f"{INSCRIPTION_ENDPOINT}/{enrollment_id}", headers=headers, timeout=TIMEOUT)
    resp.raise_for_status()
    assert resp.status_code == 200

def test_post_api_inscripciones_creates_enrollment():
    token = login()
    headers = {"Authorization": f"Bearer {token}"}

    student_id = None
    instructor_id = None
    level_id = None
    class_id = None
    enrollment_id = None

    try:
        # Create required related resources: student, instructor, level, class
        student_id = create_student(token)
        instructor_id = create_instructor(token)
        level_id = create_level(token)
        class_id = create_class(token, level_id, instructor_id)

        payload = {
            "id_estudiante": student_id,
            "id_clase": class_id
        }

        response = requests.post(INSCRIPTION_ENDPOINT, json=payload, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        assert response.status_code == 201

        enrollment = response.json()
        assert isinstance(enrollment, dict)
        assert "id" in enrollment and isinstance(enrollment["id"], int)
        assert enrollment["id_estudiante"] == student_id
        assert enrollment["id_clase"] == class_id

        enrollment_id = enrollment["id"]

    finally:
        # Cleanup enrollment first if created
        if enrollment_id:
            try:
                delete_enrollment(token, enrollment_id)
            except Exception:
                pass
        # Cleanup created class, level, instructor, student
        if class_id:
            try:
                delete_class(token, class_id)
            except Exception:
                pass
        if level_id:
            try:
                delete_level(token, level_id)
            except Exception:
                pass
        if instructor_id:
            try:
                delete_instructor(token, instructor_id)
            except Exception:
                pass
        if student_id:
            try:
                delete_student(token, student_id)
            except Exception:
                pass

test_post_api_inscripciones_creates_enrollment()
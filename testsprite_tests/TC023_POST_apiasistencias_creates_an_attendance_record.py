import requests
from datetime import date
import random
import string

BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/login"
ESTUDIANTES_URL = f"{BASE_URL}/api/estudiantes"
NIVELES_URL = f"{BASE_URL}/api/niveles"
INSTRUCTORES_URL = f"{BASE_URL}/api/instructores"
CLASES_URL = f"{BASE_URL}/api/clases"
INSCRIPCIONES_URL = f"{BASE_URL}/api/inscripciones"
ASISTENCIAS_URL = f"{BASE_URL}/api/asistencias"

# Credentials for the test user - assuming admin exists
TEST_USER_EMAIL = "admin@academia.com"
TEST_USER_PASSWORD = "admin123"

def random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))

def authenticate():
    data = {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
    response = requests.post(LOGIN_URL, json=data, timeout=30)
    assert response.status_code == 200, f"Login failed: {response.text}"
    token = response.json().get("token")
    assert token, "No token received"
    return token

def create_estudiante(token):
    headers = {"Authorization": f"Bearer {token}"}
    nombre = "TestUser_" + random_string(6)
    today_str = date.today().isoformat()
    payload = {
        "nombre": nombre,
        "fecha_nacimiento": "2000-01-01"
    }
    resp = requests.post(ESTUDIANTES_URL, json=payload, headers=headers, timeout=30)
    assert resp.status_code == 201, f"Estudiante creation failed: {resp.text}"
    return resp.json()

def delete_estudiante(token, estudiante_id):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(f"{ESTUDIANTES_URL}/{estudiante_id}", headers=headers, timeout=30)
    assert resp.status_code == 200, f"Estudiante deletion failed: {resp.text}"

def create_instructor(token):
    headers = {"Authorization": f"Bearer {token}"}
    nombre = "TestInstructor_" + random_string(6)
    payload = {
        "nombre": nombre
    }
    resp = requests.post(INSTRUCTORES_URL, json=payload, headers=headers, timeout=30)
    assert resp.status_code == 201, f"Instructor creation failed: {resp.text}"
    return resp.json()

def delete_instructor(token, instructor_id):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(f"{INSTRUCTORES_URL}/{instructor_id}", headers=headers, timeout=30)
    assert resp.status_code == 200, f"Instructor deletion failed: {resp.text}"

def get_niveles(token):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(NIVELES_URL, headers=headers, timeout=30)
    assert resp.status_code == 200, f"Get niveles failed: {resp.text}"
    niveles = resp.json()
    assert isinstance(niveles, list), "Niveles response not a list"
    return niveles

def create_clase(token, id_nivel, id_instructor):
    headers = {"Authorization": f"Bearer {token}"}
    nombre_clase = "TestClase_" + random_string(6)
    payload = {
        "nombre_clase": nombre_clase,
        "id_nivel": id_nivel,
        "id_instructor": id_instructor,
        "cupo": 10
    }
    resp = requests.post(CLASES_URL, json=payload, headers=headers, timeout=30)
    assert resp.status_code == 201, f"Clase creation failed: {resp.text}"
    return resp.json()

def delete_clase(token, clase_id):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(f"{CLASES_URL}/{clase_id}", headers=headers, timeout=30)
    assert resp.status_code == 200, f"Clase deletion failed: {resp.text}"

def create_inscripcion(token, id_estudiante, id_clase):
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "id_estudiante": id_estudiante,
        "id_clase": id_clase
    }
    resp = requests.post(INSCRIPCIONES_URL, json=payload, headers=headers, timeout=30)
    assert resp.status_code == 201, f"Inscripcion creation failed: {resp.text}"
    return resp.json()

def delete_inscripcion(token, inscripcion_id):
    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.delete(f"{INSCRIPCIONES_URL}/{inscripcion_id}", headers=headers, timeout=30)
    assert resp.status_code == 200, f"Inscripcion deletion failed: {resp.text}"

def test_post_asistencia_creates_record():
    token = authenticate()
    headers = {"Authorization": f"Bearer {token}"}
    
    # Setup resources needed: estudiante, instructor, nivel, clase, inscripcion
    
    # Create Estudiante
    estudiante = create_estudiante(token)
    estudiante_id = estudiante["id"]
    
    # Create Instructor
    instructor = create_instructor(token)
    instructor_id = instructor["id"]
    
    # Get an existing nivel or create one if none
    niveles = get_niveles(token)
    if niveles:
        nivel_id = niveles[0]["id"]
    else:
        # Create a nivel since none exist
        nombre_nivel = "TestNivel_" + random_string(6)
        resp = requests.post(NIVELES_URL, json={"nombre_nivel": nombre_nivel}, headers=headers, timeout=30)
        assert resp.status_code == 201, f"Nivel creation failed: {resp.text}"
        nivel_id = resp.json()["id"]
    
    # Create Clase
    clase = create_clase(token, nivel_id, instructor_id)
    clase_id = clase["id"]
    
    # Create Inscripcion
    inscripcion = create_inscripcion(token, estudiante_id, clase_id)
    inscripcion_id = inscripcion["id"]
    
    try:
        # Now perform the POST /api/asistencias with id_inscripcion, fecha_clase, asistio=Si
        asistencia_payload = {
            "id_inscripcion": inscripcion_id,
            "fecha_clase": date.today().isoformat(),
            "asistio": "Si"
        }
        response = requests.post(ASISTENCIAS_URL, json=asistencia_payload, headers=headers, timeout=30)
        assert response.status_code == 201, f"Failed to create asistencia: {response.text}"
        asistencia = response.json()
        # Validate fields returned match inputs
        assert asistencia.get("id_inscripcion") == inscripcion_id
        assert asistencia.get("fecha_clase") == date.today().isoformat()
        assert asistencia.get("asistio") == "Si"
    finally:
        # Cleanup created resources
        # Need to delete the asistencia record if created
        if 'asistencia' in locals() and "id" in asistencia:
            resp_del = requests.delete(f"{ASISTENCIAS_URL}/{asistencia['id']}", headers=headers, timeout=30)
            assert resp_del.status_code == 200, f"Failed to delete asistencia: {resp_del.text}"
        
        delete_inscripcion(token, inscripcion_id)
        delete_clase(token, clase_id)
        delete_instructor(token, instructor_id)
        delete_estudiante(token, estudiante_id)
        # If nivel was created newly (we have no tracking), it will be kept, since we only create if none
    
test_post_asistencia_creates_record()
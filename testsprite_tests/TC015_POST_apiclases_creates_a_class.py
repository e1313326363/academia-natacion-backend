import requests

BASE_URL = "http://localhost:8000"
LOGIN_EMAIL = "admin@academia.com"
LOGIN_PASSWORD = "admin123"
TIMEOUT = 30


def test_post_api_clases_creates_class():
    # Authenticate to obtain Bearer token
    login_url = f"{BASE_URL}/api/login"
    login_payload = {"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
    login_response = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    token = login_response.json().get("token")
    assert token is not None, "No token returned from login"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Helper: Get or create a Nivel
    def get_or_create_nivel():
        niveles_resp = requests.get(f"{BASE_URL}/api/niveles", headers=headers, timeout=TIMEOUT)
        assert niveles_resp.status_code == 200, f"Failed to get niveles: {niveles_resp.text}"
        niveles = niveles_resp.json()
        if niveles:
            return niveles[0]["id"] if "id" in niveles[0] else niveles[0]["ID"] if "ID" in niveles[0] else niveles[0].get("id")
        # Create Nivel if none exist
        nivel_payload = {"nombre_nivel": "TestNivel_12345"}
        resp = requests.post(f"{BASE_URL}/api/niveles", headers=headers, json=nivel_payload, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Failed to create nivel: {resp.text}"
        return resp.json()["id"]

    # Helper: Create an Instructor
    def create_instructor():
        instructor_payload = {"nombre": "Test Instructor 12345"}
        resp = requests.post(f"{BASE_URL}/api/instructores", headers=headers, json=instructor_payload, timeout=TIMEOUT)
        assert resp.status_code == 201, f"Failed to create instructor: {resp.text}"
        return resp.json()["id"]

    id_nivel = get_or_create_nivel()
    id_instructor = create_instructor()

    clase_payload = {
        "nombre_clase": "Clase de Prueba 12345",
        "id_nivel": id_nivel,
        "id_instructor": id_instructor,
        "cupo": 20
    }

    class_id = None
    try:
        response = requests.post(f"{BASE_URL}/api/clases", headers=headers, json=clase_payload, timeout=TIMEOUT)
        assert response.status_code == 201, f"Expected 201 but got {response.status_code} with body {response.text}"
        data = response.json()
        assert "id" in data or "ID" in data, "Response missing class id"
        # Save id for cleanup
        class_id = data.get("id") or data.get("ID")
        assert data.get("nombre_clase") == clase_payload["nombre_clase"], "nombre_clase mismatch"
        assert data.get("id_nivel") == clase_payload["id_nivel"], "id_nivel mismatch"
        assert data.get("id_instructor") == clase_payload["id_instructor"], "id_instructor mismatch"
        assert data.get("cupo") == clase_payload["cupo"], "cupo mismatch"
    finally:
        # Cleanup: Delete created class
        if class_id is not None:
            del_resp = requests.delete(f"{BASE_URL}/api/clases/{class_id}", headers=headers, timeout=TIMEOUT)
            assert del_resp.status_code == 200, f"Cleanup failed, could not delete class: {del_resp.text}"
        # Cleanup: Delete created instructor
        if id_instructor is not None:
            del_inst_resp = requests.delete(f"{BASE_URL}/api/instructores/{id_instructor}", headers=headers, timeout=TIMEOUT)
            assert del_inst_resp.status_code == 200, f"Cleanup failed, could not delete instructor: {del_inst_resp.text}"
        # Cleanup: Delete created nivel if it was created just now
        # To avoid deleting an existing nivel, only delete if nivel name was "TestNivel_12345"
        niveles_resp = requests.get(f"{BASE_URL}/api/niveles", headers=headers, timeout=TIMEOUT)
        if niveles_resp.status_code == 200:
            niveles = niveles_resp.json()
            for nivel in niveles:
                nivel_id = nivel.get("id") or nivel.get("ID")
                nivel_nombre = nivel.get("nombre_nivel") or nivel.get("nombreNivel")
                if nivel_id == id_nivel and nivel_nombre == "TestNivel_12345":
                    del_nivel_resp = requests.delete(f"{BASE_URL}/api/niveles/{nivel_id}", headers=headers, timeout=TIMEOUT)
                    assert del_nivel_resp.status_code == 200, f"Cleanup failed, could not delete nivel: {del_nivel_resp.text}"
                    break


test_post_api_clases_creates_class()
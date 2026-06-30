import requests
import datetime

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = "/api/login"
PAGOS_ENDPOINT = "/api/pagos"
INSCRIPCIONES_ENDPOINT = "/api/inscripciones"
LOGOUT_ENDPOINT = "/api/logout"

EMAIL = "admin@academia.com"
PASSWORD = "admin123"
TIMEOUT = 30

def test_post_api_pagos_creates_payment():
    # Authenticate to get Bearer token
    login_payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    login_response = requests.post(f"{BASE_URL}{LOGIN_ENDPOINT}", json=login_payload, timeout=TIMEOUT)
    assert login_response.status_code == 200, f"Login failed: {login_response.text}"
    token = login_response.json().get("token")
    assert token, "No token found in login response"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Create a new inscripcion (enrollment) resource to use its id_inscripcion for the payment
    # Need a valid id_estudiante and id_clase for creating inscripcion
    # We'll retrieve first available estudiante and clase
    # Get estudiantes
    estudiantes_resp = requests.get(f"{BASE_URL}/api/estudiantes?page=1&per_page=1", headers=headers, timeout=TIMEOUT)
    assert estudiantes_resp.status_code == 200, f"Failed to get estudiantes: {estudiantes_resp.text}"
    estudiantes_data = estudiantes_resp.json()
    estudiantes_list = estudiantes_data.get("data") if isinstance(estudiantes_data, dict) else None
    assert estudiantes_list and len(estudiantes_list) > 0, "No estudiantes found to create inscripcion"
    id_estudiante = estudiantes_list[0].get("id")
    assert id_estudiante, "Estudiante id not found"

    # Get clases
    clases_resp = requests.get(f"{BASE_URL}/api/clases?page=1&per_page=1", headers=headers, timeout=TIMEOUT)
    assert clases_resp.status_code == 200, f"Failed to get clases: {clases_resp.text}"
    clases_data = clases_resp.json()
    clases_list = clases_data.get("data") if isinstance(clases_data, dict) else None
    assert clases_list and len(clases_list) > 0, "No clases found to create inscripcion"
    id_clase = clases_list[0].get("id")
    assert id_clase, "Clase id not found"

    created_inscripcion_id = None
    created_pago_id = None

    try:
        # Create inscripcion
        inscripcion_payload = {
            "id_estudiante": id_estudiante,
            "id_clase": id_clase,
        }
        inscripcion_resp = requests.post(f"{BASE_URL}{INSCRIPCIONES_ENDPOINT}", json=inscripcion_payload, headers=headers, timeout=TIMEOUT)
        assert inscripcion_resp.status_code == 201, f"Failed to create inscripcion: {inscripcion_resp.text}"
        inscripcion = inscripcion_resp.json()
        created_inscripcion_id = inscripcion.get("id")
        assert created_inscripcion_id, "Created inscripcion id missing"

        # Prepare pago payload
        pago_payload = {
            "id_inscripcion": created_inscripcion_id,
            "monto": 100.50,
            "metodo_pago": "Efectivo"
        }

        pago_resp = requests.post(f"{BASE_URL}{PAGOS_ENDPOINT}", json=pago_payload, headers=headers, timeout=TIMEOUT)
        assert pago_resp.status_code == 201, f"Failed to create pago: {pago_resp.text}"
        pago_data = pago_resp.json()
        created_pago_id = pago_data.get("id")
        assert created_pago_id is not None, "Created pago id missing"

        # Validate response fields
        assert pago_data.get("id_inscripcion") == created_inscripcion_id
        assert float(pago_data.get("monto", 0)) == pago_payload["monto"]
        assert pago_data.get("metodo_pago") == pago_payload["metodo_pago"]
    finally:
        # Cleanup: delete created pago and inscripcion if they exist
        if created_pago_id:
            del_pago_resp = requests.delete(f"{BASE_URL}{PAGOS_ENDPOINT}/{created_pago_id}", headers=headers, timeout=TIMEOUT)
            assert del_pago_resp.status_code == 200, f"Failed to delete pago during cleanup: {del_pago_resp.text}"
        if created_inscripcion_id:
            del_inscripcion_resp = requests.delete(f"{BASE_URL}{INSCRIPCIONES_ENDPOINT}/{created_inscripcion_id}", headers=headers, timeout=TIMEOUT)
            assert del_inscripcion_resp.status_code == 200, f"Failed to delete inscripcion during cleanup: {del_inscripcion_resp.text}"

    # Optional: logout
    logout_resp = requests.post(f"{BASE_URL}{LOGOUT_ENDPOINT}", headers=headers, timeout=TIMEOUT)
    assert logout_resp.status_code == 200, f"Logout failed: {logout_resp.text}"

test_post_api_pagos_creates_payment()
import requests

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{BASE_URL}/api/login"
CLASES_ENDPOINT = f"{BASE_URL}/api/clases"
NIVELES_ENDPOINT = f"{BASE_URL}/api/niveles"
INSTRUCTORES_ENDPOINT = f"{BASE_URL}/api/instructores"
TIMEOUT = 30

EMAIL = "admin@academia.com"  # Replace with valid admin email if needed
PASSWORD = "admin123"         # Replace with valid admin password if needed


def test_post_clases_with_invalid_cupo_returns_422():
    # Authenticate and get Bearer token
    login_payload = {"email": EMAIL, "password": PASSWORD}
    login_resp = requests.post(LOGIN_ENDPOINT, json=login_payload, timeout=TIMEOUT)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token = login_resp.json().get("token")
    assert token, "No token received on login"

    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Get existing id_nivel from /api/niveles
    niveles_resp = requests.get(NIVELES_ENDPOINT, headers=headers, timeout=TIMEOUT)
    assert niveles_resp.status_code == 200, f"Failed to get niveles: {niveles_resp.text}"
    niveles = niveles_resp.json()
    assert isinstance(niveles, list) and len(niveles) > 0, "No niveles found"
    id_nivel = niveles[0]["id"] if "id" in niveles[0] else niveles[0].get("id_nivel", None)
    assert id_nivel is not None, "id_nivel not found in niveles"

    # Get existing id_instructor from /api/instructores
    instructores_resp = requests.get(INSTRUCTORES_ENDPOINT, headers=headers, timeout=TIMEOUT)
    assert instructores_resp.status_code == 200, f"Failed to get instructores: {instructores_resp.text}"
    instructores_data = instructores_resp.json()
    instructores = instructores_data.get("data") if isinstance(instructores_data, dict) else instructores_data
    assert isinstance(instructores, list) and len(instructores) > 0, "No instructores found"
    id_instructor = instructores[0].get("id")
    assert id_instructor is not None, "id_instructor not found in instructores"

    # Prepare invalid cupo values to test
    invalid_cupos = [0, 100]

    for cupo in invalid_cupos:
        clase_payload = {
            "nombre_clase": f"Clase Test Invalid Cupo {cupo}",
            "id_nivel": id_nivel,
            "id_instructor": id_instructor,
            "cupo": cupo
        }
        resp = requests.post(CLASES_ENDPOINT, headers=headers, json=clase_payload, timeout=TIMEOUT)
        assert resp.status_code == 422, (
            f"Expected 422 for cupo={cupo}, got {resp.status_code}. Response: {resp.text}"
        )


test_post_clases_with_invalid_cupo_returns_422()
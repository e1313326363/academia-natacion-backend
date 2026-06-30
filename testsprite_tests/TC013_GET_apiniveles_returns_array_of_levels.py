import requests

BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/login"
NIVELES_URL = f"{BASE_URL}/api/niveles"

EMAIL = "admin@academia.com"
PASSWORD = "admin123"
TIMEOUT = 30

def test_get_niveles_returns_array_of_levels():
    # Authenticate to get Bearer token
    login_payload = {"email": EMAIL, "password": PASSWORD}
    login_resp = requests.post(LOGIN_URL, json=login_payload, timeout=TIMEOUT)
    assert login_resp.status_code == 200, f"Login failed with status code {login_resp.status_code}"
    login_data = login_resp.json()
    token = login_data.get("token")
    assert token, "No token received from login"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # GET /api/niveles
    niveles_resp = requests.get(NIVELES_URL, headers=headers, timeout=TIMEOUT)
    assert niveles_resp.status_code == 200, f"Expected 200 but got {niveles_resp.status_code}"
    niveles_data = niveles_resp.json()
    assert isinstance(niveles_data, list), f"Response is not an array: {type(niveles_data)}"

    # Check the response contains at least 4 levels including required names
    nombres_nivel = [nivel.get("nombre_nivel") or nivel.get("nombre") or nivel.get("nombreNivel") or nivel.get("nombreNivel") for nivel in niveles_data if isinstance(nivel, dict)]
    required_levels = {"Principiante", "Intermedio", "Avanzado", "Competencia"}
    found_levels = set(n for n in nombres_nivel if n in required_levels)
    assert len(niveles_data) >= 4, f"Expected at least 4 levels but got {len(niveles_data)}"
    assert found_levels == required_levels, f"Expected levels {required_levels} but found {found_levels}"

test_get_niveles_returns_array_of_levels()
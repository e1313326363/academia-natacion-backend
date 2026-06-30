import requests

BASE_URL = "http://localhost:8000"
LOGIN_EMAIL = "admin@academia.com"
LOGIN_PASSWORD = "admin123"
TIMEOUT = 30

def test_get_clases_returns_paginated_list_with_nivel_and_instructor():
    # Authenticate to get Bearer token
    login_url = f"{BASE_URL}/api/login"
    login_payload = {
        "email": LOGIN_EMAIL,
        "password": LOGIN_PASSWORD
    }
    login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token = login_resp.json().get("token")
    assert token and isinstance(token, str), "Token missing or invalid"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    # Call GET /api/clases endpoint
    clases_url = f"{BASE_URL}/api/clases"
    resp = requests.get(clases_url, headers=headers, timeout=TIMEOUT)
    assert resp.status_code == 200, f"GET /api/clases failed: {resp.text}"

    data = resp.json()

    # Validate paginated structure: should have 'data', 'current_page', 'last_page', 'per_page', 'total' typically
    assert "data" in data and isinstance(data["data"], list), "Missing or invalid 'data' field"
    assert "current_page" in data and isinstance(data["current_page"], int), "Missing or invalid 'current_page' field"
    assert "last_page" in data and isinstance(data["last_page"], int), "Missing or invalid 'last_page' field"

    # For each class item, validate it includes nested nivel and instructor objects
    for clase in data["data"]:
        # Validate clase is a dict
        assert isinstance(clase, dict), "Clase item is not a dictionary"

        # Validate nested 'nivel'
        nivel = clase.get("nivel")
        assert nivel is not None, "Clase missing 'nivel' field"
        assert isinstance(nivel, dict), "'nivel' field is not a dictionary"
        # At minimum, nivel should have an 'id' and 'nombre_nivel' or similar
        assert "id" in nivel and isinstance(nivel["id"], int), "'nivel.id' missing or not int"
        assert "nombre_nivel" in nivel and isinstance(nivel["nombre_nivel"], str), "'nivel.nombre_nivel' missing or not str"

        # Validate nested 'instructor'
        instructor = clase.get("instructor")
        assert instructor is not None, "Clase missing 'instructor' field"
        assert isinstance(instructor, dict), "'instructor' field is not a dictionary"
        # At minimum, instructor should have 'id' and 'nombre' or similar
        assert "id" in instructor and isinstance(instructor["id"], int), "'instructor.id' missing or not int"
        assert "nombre" in instructor and isinstance(instructor["nombre"], str), "'instructor.nombre' missing or not str"


test_get_clases_returns_paginated_list_with_nivel_and_instructor()
import requests

BASE_URL = "http://localhost:8000"
LOGIN_EMAIL = "admin@academia.com"
LOGIN_PASSWORD = "admin123"
TIMEOUT = 30

def authenticate():
    url = f"{BASE_URL}/api/login"
    payload = {"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
    response = requests.post(url, json=payload, timeout=TIMEOUT)
    response.raise_for_status()
    token = response.json().get("token")
    assert token, "Token not found in login response"
    return token

def test_get_asistencias_returns_paginated_attendance_records():
    token = authenticate()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{BASE_URL}/api/asistencias"
    params = {"page": 1}
    response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    data = response.json()
    # Check for pagination keys
    assert isinstance(data, dict), "Response is not a dict"
    # Usually paginated responses have 'data', 'current_page', 'last_page', 'total'
    assert "data" in data and isinstance(data["data"], list), "'data' field missing or not a list"
    assert "current_page" in data and isinstance(data["current_page"], int), "'current_page' missing or not int"
    assert "last_page" in data and isinstance(data["last_page"], int), "'last_page' missing or not int"
    assert "total" in data and isinstance(data["total"], int), "'total' missing or not int"
    # Check fields in attendance records
    for record in data["data"]:
        assert isinstance(record, dict), "Attendance record is not a dict"
        # Check fecha_clase field presence and type
        assert "fecha_clase" in record, "'fecha_clase' field missing in attendance record"
        # fecha_clase should be a string (date)
        assert isinstance(record["fecha_clase"], str), "'fecha_clase' is not a string"
        # Check asistio field presence and type
        assert "asistio" in record, "'asistio' field missing in attendance record"
        # asistio should be "Si" or "No"
        assert record["asistio"] in ["Si", "No"], f"Invalid value for asistio: {record['asistio']}"

test_get_asistencias_returns_paginated_attendance_records()
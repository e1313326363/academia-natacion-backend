import requests

BASE_URL = "http://localhost:8000"
LOGIN_EMAIL = "admin@academia.com"
LOGIN_PASSWORD = "admin123"
TIMEOUT = 30

def test_get_pagos_returns_paginated_payments():
    # Authenticate and get token
    login_url = f"{BASE_URL}/api/login"
    login_payload = {"email": LOGIN_EMAIL, "password": LOGIN_PASSWORD}
    try:
        login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
        assert login_resp.status_code == 200, f"Login failed with status {login_resp.status_code}"
        token = login_resp.json().get("token")
        assert token, "No token found in login response"
    except Exception as e:
        assert False, f"Login request failed: {e}"

    headers = {"Authorization": f"Bearer {token}"}
    pagos_url = f"{BASE_URL}/api/pagos"
    params = {"page": 1}

    try:
        response = requests.get(pagos_url, headers=headers, params=params, timeout=TIMEOUT)
        assert response.status_code == 200, f"GET /api/pagos returned status {response.status_code}"
        data = response.json()
        # Confirm presence of pagination fields typically expected
        # (e.g. data, total, current_page, last_page)
        assert "data" in data, "'data' field missing in response"
        assert isinstance(data["data"], list), "'data' is not a list"
        # Validate each payment item for monto, metodo_pago, and estado fields
        for payment in data["data"]:
            assert "monto" in payment, "Field 'monto' missing in payment item"
            assert isinstance(payment["monto"], (int, float)), "'monto' is not numeric"
            assert "metodo_pago" in payment, "Field 'metodo_pago' missing in payment item"
            assert isinstance(payment["metodo_pago"], str), "'metodo_pago' is not string"
            assert "estado" in payment, "Field 'estado' missing in payment item"
            assert isinstance(payment["estado"], str), "'estado' is not string"
    except Exception as e:
        assert False, f"Request or validation failed: {e}"

test_get_pagos_returns_paginated_payments()
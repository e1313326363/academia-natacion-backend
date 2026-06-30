import requests

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{BASE_URL}/api/login"
DASHBOARD_STATS_ENDPOINT = f"{BASE_URL}/api/dashboard/stats"

def test_get_dashboard_stats_returns_counts():
    # Credentials for authentication (from PRD instructions)
    auth_payload = {
        "email": "admin@academia.com",
        "password": "admin123"
    }
    try:
        # Authenticate to get Bearer token
        login_resp = requests.post(LOGIN_ENDPOINT, json=auth_payload, timeout=30)
        assert login_resp.status_code == 200, f"Login failed with status {login_resp.status_code}"
        login_data = login_resp.json()
        token = login_data.get("token")
        assert token and isinstance(token, str), "Token not found or invalid in login response"

        headers = {
            "Authorization": f"Bearer {token}"
        }

        # Call dashboard stats endpoint
        resp = requests.get(DASHBOARD_STATS_ENDPOINT, headers=headers, timeout=30)
        assert resp.status_code == 200, f"Dashboard stats returned unexpected status: {resp.status_code}"

        data = resp.json()
        # Validate all required keys present and are integers
        for key in ("estudiantes", "instructores", "clases", "inscripciones_activas"):
            assert key in data, f"Missing key '{key}' in dashboard stats response"
            value = data[key]
            assert isinstance(value, int), f"Value for '{key}' is not an int: got {type(value)}"
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

test_get_dashboard_stats_returns_counts()
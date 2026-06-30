import requests

BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/api/login"
LOGOUT_URL = f"{BASE_URL}/api/logout"
ME_URL = f"{BASE_URL}/api/me"
TIMEOUT = 30

def test_post_api_logout_revokes_token():
    login_payload = {
        "email": "admin@academia.com",
        "password": "admin123"
    }
    # Step 1: Login to get the token
    try:
        login_resp = requests.post(LOGIN_URL, json=login_payload, timeout=TIMEOUT)
        assert login_resp.status_code == 200, f"Login failed with status {login_resp.status_code}"
        login_data = login_resp.json()
        token = login_data.get("token")
        assert token, "Token not found in login response"
        headers = {"Authorization": f"Bearer {token}"}

        # Step 2: Call POST /api/logout to revoke the token
        logout_resp = requests.post(LOGOUT_URL, headers=headers, timeout=TIMEOUT)
        assert logout_resp.status_code == 200, f"Logout failed with status {logout_resp.status_code}"
        logout_json = logout_resp.json()
        assert "message" in logout_json and isinstance(logout_json["message"], str), "Logout response missing message"

        # Step 3: Call GET /api/me with the same token after logout - should return 401 Unauthorized
        me_resp = requests.get(ME_URL, headers=headers, timeout=TIMEOUT)
        assert me_resp.status_code == 401, f"Expected 401 after logout but got {me_resp.status_code}"

    except requests.RequestException as e:
        assert False, f"RequestException occurred: {e}"

test_post_api_logout_revokes_token()
import requests

BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = "/api/login"
ME_ENDPOINT = "/api/me"
TIMEOUT = 30

def test_get_api_me_returns_authenticated_user():
    login_payload = {
        "email": "admin@academia.com",
        "password": "admin123"
    }
    try:
        # Login to get Bearer token
        login_response = requests.post(
            BASE_URL + LOGIN_ENDPOINT,
            json=login_payload,
            timeout=TIMEOUT
        )
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"
        login_data = login_response.json()
        token = login_data.get("token")
        user = login_data.get("user")
        assert token and isinstance(token, str), "Token missing or invalid in login response"
        assert user and isinstance(user, dict), "User data missing or invalid in login response"

        headers = {
            "Authorization": f"Bearer {token}"
        }
        # GET /api/me with valid token
        me_response = requests.get(
            BASE_URL + ME_ENDPOINT,
            headers=headers,
            timeout=TIMEOUT
        )
        assert me_response.status_code == 200, f"GET /api/me failed: {me_response.text}"
        me_data = me_response.json()
        # Validate that name, email, and role match those in login user data
        assert "name" in me_data, "'name' field missing in /api/me response"
        assert "email" in me_data, "'email' field missing in /api/me response"
        assert "role" in me_data, "'role' field missing in /api/me response"
        assert me_data["name"] == user.get("name"), "Name mismatch between login and /api/me"
        assert me_data["email"] == user.get("email"), "Email mismatch between login and /api/me"
        assert me_data["role"] == user.get("role"), "Role mismatch between login and /api/me"

    finally:
        # Logout to revoke token if possible
        logout_endpoint = "/api/logout"
        if 'token' in locals():
            try:
                headers = {"Authorization": f"Bearer {token}"}
                requests.post(BASE_URL+logout_endpoint, headers=headers, timeout=TIMEOUT)
            except Exception:
                pass

test_get_api_me_returns_authenticated_user()
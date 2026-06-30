import requests

def test_post_api_login_with_invalid_credentials_returns_401():
    base_url = "http://localhost:8000"
    url = f"{base_url}/api/login"
    payload = {
        "email": "admin@academia.com",
        "password": "wrongpassword123"
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"
        # Check response content to include "Invalid credentials" (case insensitive)
        assert "invalid credentials" in response.text.lower(), "Response does not contain 'Invalid credentials' message."
    except requests.RequestException as e:
        assert False, f"Request to {url} failed with exception: {e}"

test_post_api_login_with_invalid_credentials_returns_401()
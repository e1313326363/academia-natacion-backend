import requests

def test_unauthenticated_request_returns_401():
    base_url = "http://localhost:8000"
    url = f"{base_url}/api/estudiantes"

    try:
        response = requests.get(url, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 401, f"Expected status 401 but got {response.status_code}"
    # Optionally check response content for unauthorized message
    try:
        json_data = response.json()
        assert "message" in json_data or "error" in json_data or json_data == {}, "Expected error message or empty response"
    except ValueError:
        pass  # response is not json, no further checks

test_unauthenticated_request_returns_401()
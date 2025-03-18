import os

from dotenv import load_dotenv
from fastapi.testclient import TestClient
from src.token_utils import create_access_token, create_refresh_token

load_dotenv()
ID_FIELD = os.getenv("ID_FIELD", "")

# THERE IS NO WAY TO CREATE TOKEN WITH WRONG GUID
TEST_USER_ID = "asdasd"
DATA = {
    ID_FIELD: TEST_USER_ID,
}
AUTH_DATA = {
    # "code_verifier": "front"
    "code_challenge": "LY1pMXesRIlfwCwAnsP2rzLlHrAHg8FwANcFHRZiuTo",
    "code_challenge_method": "string",
}


# Helper functions to generate tokens
def generate_valid_access_token():
    return create_access_token(DATA)


def generate_valid_refresh_token():
    return create_refresh_token(DATA)


def generate_expired_access_token():
    return create_access_token(DATA, expiration_minutes=-1)


def generate_expired_refresh_token():
    return create_refresh_token(DATA, expiration_days=-1)


def test_auth_with_no_tokens(client: TestClient, override_db_dependency):
    response = client.post("/auth/auth", json=AUTH_DATA)
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_auth_with_valid_access_token(
    client: TestClient, override_db_dependency
):
    access_token = generate_valid_access_token()
    client.cookies.set("access_token", access_token)
    response = client.post("/auth/auth", json=AUTH_DATA)
    assert response.status_code == 200
    assert response.json() == TEST_USER_ID


def test_auth_with_only_refresh_token(
    client: TestClient, override_db_dependency
):
    client.cookies.clear()
    refresh_token = generate_valid_refresh_token()
    client.cookies.set("refresh_token", refresh_token)
    response = client.post("/auth/auth", json=AUTH_DATA)
    assert response.status_code == 200
    assert response.json() == TEST_USER_ID
    assert "access_token" in response.cookies


def test_auth_with_expired_access_token_and_valid_refresh_token(
    client: TestClient, override_db_dependency
):
    client.cookies.clear()
    access_token = generate_expired_access_token()
    refresh_token = generate_valid_refresh_token()
    client.cookies.set("refresh_token", refresh_token)
    client.cookies.set("access_token", access_token)
    response = client.post("/auth/auth", json=AUTH_DATA)
    assert response.status_code == 200
    assert response.json() == TEST_USER_ID
    assert "access_token" in response.cookies


def test_auth_with_invalid_refresh_token(
    client: TestClient, override_db_dependency
):
    client.cookies.clear()
    access_token = generate_expired_access_token()
    refresh_token = "invalid_refresh_token"
    client.cookies.set("refresh_token", refresh_token)
    client.cookies.set("access_token", access_token)
    response = client.post("/auth/auth", json=AUTH_DATA)
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_auth_with_expired_refresh_token(
    client: TestClient, override_db_dependency
):
    client.cookies.clear()
    access_token = generate_expired_access_token()
    refresh_token = generate_expired_refresh_token()
    client.cookies.set("refresh_token", refresh_token)
    client.cookies.set("access_token", access_token)
    response = client.post("/auth/auth", json=AUTH_DATA)
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]

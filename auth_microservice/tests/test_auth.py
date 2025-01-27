import os
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.routers.auth_router import auth_router
from src.token_utils import (
    create_access_token,
    create_refresh_token,
)
from dotenv import load_dotenv

load_dotenv()
ID_FIELD = os.getenv("ID_FIELD", "")
app = FastAPI()
app.include_router(auth_router)

client = TestClient(app)

# THERE IS NO WAY TO CREATE TOKEN WITH WRONG GUID
TEST_USER_ID = "asdasd"
DATA = {
    ID_FIELD: TEST_USER_ID,
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


def test_auth_with_valid_access_token():
    client.cookies.clear()
    access_token = generate_valid_access_token()
    response = client.get("/auth", cookies={"access_token": access_token})
    assert response.status_code == 200
    assert response.json() == TEST_USER_ID


def test_auth_with_expired_access_token_and_valid_refresh_token():
    client.cookies.clear()
    access_token = generate_expired_access_token()
    refresh_token = generate_valid_refresh_token()
    response = client.get(
        "/auth",
        cookies={"access_token": access_token, "refresh_token": refresh_token},
    )
    assert response.status_code == 200
    assert response.json() == TEST_USER_ID
    assert "access_token" in response.cookies


def test_auth_with_no_tokens():
    client.cookies.clear()
    response = client.get("/auth")
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_auth_with_invalid_refresh_token():
    client.cookies.clear()
    access_token = generate_expired_access_token()
    refresh_token = "invalid_refresh_token"
    response = client.get(
        "/auth",
        cookies={"access_token": access_token, "refresh_token": refresh_token},
    )
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_auth_with_expired_refresh_token():
    client.cookies.clear()
    access_token = generate_expired_access_token()
    refresh_token = generate_expired_refresh_token()
    response = client.get(
        "/auth",
        cookies={"access_token": access_token, "refresh_token": refresh_token},
    )
    assert response.status_code == 401
    assert "Not authenticated" in response.json()["detail"]


def test_auth_with_only_refresh_token():
    client.cookies.clear()
    refresh_token = generate_valid_refresh_token()
    response = client.get("/auth", cookies={"refresh_token": refresh_token})
    assert response.status_code == 200
    assert response.json() == TEST_USER_ID
    assert "access_token" in response.cookies

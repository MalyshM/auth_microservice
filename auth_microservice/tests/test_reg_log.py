from fastapi.testclient import TestClient
import pytest

TEST_USER = {
    "email": "test@example.com",
    "password": "asdASD123!@#",
}


@pytest.mark.asyncio
async def test_register_user(client: TestClient, override_db_dependency):
    response = client.post("/register", json=TEST_USER)
    assert response.status_code == 200
    assert client.cookies.get("refresh_token")
    assert response.json()["email"] == TEST_USER["email"]


@pytest.mark.asyncio
async def test_register_duplicate_user(
    client: TestClient, override_db_dependency
):
    assert client.cookies.get("refresh_token") is None
    client.post("/register", json=TEST_USER)
    assert client.cookies.get("refresh_token")
    response = client.post("/register", json=TEST_USER)
    assert response.status_code == 200
    assert client.cookies.get("refresh_token")
    assert client.cookies.get("access_token")
    rsp = response.json()
    assert isinstance(rsp, list)
    assert isinstance(rsp[0], dict)
    assert rsp[0]["email"] == TEST_USER["email"]


# Test successful user login
# @pytest.mark.asyncio
# async def test_login_user(client: TestClient, override_db_dependency):
#     # Register the user first
#     client.post("/register", json=TEST_USER)

#     # Login with the same credentials
#     response = client.post("/login", json=TEST_USER)
#     assert response.status_code == 200
#     assert response.json()["email"] == TEST_USER["email"]


# # Test login with incorrect password
# @pytest.mark.asyncio
# async def test_login_incorrect_password(client: TestClient, override_db_dependency):
#     # Register the user first
#     client.post("/register", json=TEST_USER)

#     # Login with incorrect password
#     incorrect_credentials = {**TEST_USER, "password": "wrongpassword"}
#     response = client.post("/login", json=incorrect_credentials)
#     assert response.status_code == 403
#     assert "incorrect data" in response.json()["detail"]


# # Test login with non-existent user
# @pytest.mark.asyncio
# async def test_login_nonexistent_user(client: TestClient, override_db_dependency):
#     # Try to login with a user that doesn't exist
#     response = client.post("/login", json=TEST_USER)
#     assert response.status_code == 404
#     assert "not found" in response.json()["detail"]


# # Test database error during registration
# @pytest.mark.asyncio
# async def test_register_database_error(
#     client: TestClient, override_db_dependency, async_session
# ):
#     # Simulate a database error
#     async with async_session() as session:
#         session.add(UserDBType(**TEST_USER))
#         await session.commit()

#     # Try to register the same user again
#     response = client.post("/register", json=TEST_USER)
#     assert response.status_code == 400
#     assert "could not be registered" in response.json()["detail"]

from fastapi.testclient import TestClient

TEST_USER = {
    "email": "test@example.com",
    "password": "asdASD123!@#",
}
TEST_USER_NOT_EXISTS = {
    "email": "testtest@example.com",
    "password": "asdASD123!@#",
}


async def test_register_existing_user(
    client: TestClient, override_db_dependency
):
    assert client.cookies.get("refresh_token") is None
    client.post("/register", json=TEST_USER)
    assert client.cookies.get("refresh_token")
    client.cookies.delete("refresh_token")
    response = client.post("/register", json=TEST_USER)
    assert response.status_code == 200
    assert client.cookies.get("refresh_token")
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert rsp["email"] == TEST_USER["email"]


async def test_register_existing_user_wrong_password(
    client: TestClient, override_db_dependency
):
    assert client.cookies.get("refresh_token") is None
    client.post("/register", json=TEST_USER)
    assert client.cookies.get("refresh_token")
    client.cookies.delete("refresh_token")
    incorrect_credentials = {**TEST_USER, "password": "asdASD123!@#wrong"}
    response = client.post("/register", json=incorrect_credentials)
    assert response.status_code == 400
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert "could not be registered" in rsp["detail"]


async def test_register_user(client: TestClient, override_db_dependency):
    response = client.post("/register", json=TEST_USER)
    assert response.status_code == 200
    assert client.cookies.get("refresh_token")
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert rsp["email"] == TEST_USER["email"]


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
    assert isinstance(rsp, dict)
    assert rsp["email"] == TEST_USER["email"]


async def test_login_user(client: TestClient, override_db_dependency):
    assert client.cookies.get("refresh_token") is None
    client.post("/register", json=TEST_USER)
    assert client.cookies.get("refresh_token")
    response = client.post("/login", json=TEST_USER)
    assert response.status_code == 200
    assert client.cookies.get("refresh_token")
    assert client.cookies.get("access_token")
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert rsp["email"] == TEST_USER["email"]


async def test_login_incorrect_password_with_refresh_token(
    client: TestClient, override_db_dependency
):
    assert client.cookies.get("refresh_token") is None
    client.post("/register", json=TEST_USER)
    assert client.cookies.get("refresh_token")
    client.post("/logout", json=TEST_USER)
    assert not client.cookies.get("refresh_token")
    assert not client.cookies.get("access_token")
    incorrect_credentials = {**TEST_USER, "password": "asdASD123!@#wrong"}
    response = client.post("/login", json=incorrect_credentials)
    assert response.status_code == 403
    assert not client.cookies.get("refresh_token")
    assert not client.cookies.get("access_token")
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert "incorrect" in rsp["detail"]


async def test_login_incorrect_password(
    client: TestClient, override_db_dependency
):
    assert client.cookies.get("refresh_token") is None
    client.post("/register", json=TEST_USER)
    assert client.cookies.get("refresh_token")
    client.post("/logout", json=TEST_USER)
    assert not client.cookies.get("refresh_token")
    assert not client.cookies.get("access_token")
    incorrect_credentials = {**TEST_USER, "password": "asdASD123!@#wrong"}
    response = client.post("/login", json=incorrect_credentials)
    assert response.status_code == 403
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert "incorrect" in rsp["detail"]


async def test_login_correct_password(
    client: TestClient, override_db_dependency
):
    assert client.cookies.get("refresh_token") is None
    client.post("/register", json=TEST_USER)
    assert client.cookies.get("refresh_token")
    client.cookies.delete("refresh_token")
    response = client.post("/login", json=TEST_USER)
    assert response.status_code == 200
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert rsp["email"] == TEST_USER["email"]


async def test_login_incorrect_user(
    client: TestClient, override_db_dependency
):
    assert client.cookies.get("refresh_token") is None
    response = client.post("/login", json=TEST_USER_NOT_EXISTS)
    assert response.status_code == 404
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert "User not found" in rsp["detail"]

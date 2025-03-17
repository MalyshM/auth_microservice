import pytest
from fastapi.testclient import TestClient

# Test data
TEST_USER_FOR_TOKEN = {
    "email": "test_for_token@example.com",
    "password": "asdASD123!@#",
}
TEST_USER = {
    "email": "test@example.com",
    "password": "asdASD123!@#",
}
TEST_USER_UPDATE = {
    "email": "updated@example.com",
    "username": "Updated",
}

TEST_USER_UPDATE_ERR = {
    "email": "test_for_token@example.com",
    "username": "Updated",
}


def registrer_user(client: TestClient, override_db_dependency):
    assert client.cookies.get("refresh_token") is None
    client.post("/register", json=TEST_USER_FOR_TOKEN)
    assert client.cookies.get("refresh_token")


@pytest.mark.asyncio
async def test_create_user(client: TestClient, override_db_dependency):
    registrer_user(client, override_db_dependency)
    response = client.post("/user", json=TEST_USER)
    assert client.cookies.get("access_token")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["email"] == TEST_USER["email"]


@pytest.mark.asyncio
async def test_create_user_error(client: TestClient, override_db_dependency):
    registrer_user(client, override_db_dependency)
    response = client.post("/user", json=TEST_USER_FOR_TOKEN)
    assert response.status_code == 400
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert "User could not be created" in rsp["detail"]


@pytest.mark.asyncio
async def test_get_users(client: TestClient, override_db_dependency):
    registrer_user(client, override_db_dependency)
    response = client.get("/user")
    assert client.cookies.get("access_token")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    for user in data:
        assert user["email"] in [
            TEST_USER["email"],
            TEST_USER_FOR_TOKEN["email"],
        ]


@pytest.mark.asyncio
async def test_get_my_user(client: TestClient, override_db_dependency):
    registrer_user(client, override_db_dependency)
    client.post("/user", json=TEST_USER)
    response = client.get("/user/me")
    assert client.cookies.get("access_token")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["email"] == TEST_USER_FOR_TOKEN["email"]


@pytest.mark.asyncio
async def test_get_user_by_id(client: TestClient, override_db_dependency):
    registrer_user(client, override_db_dependency)
    create_response = client.post("/user", json=TEST_USER)
    user_id = create_response.json()["id"]
    response = client.get(f"/user/{user_id}")
    assert client.cookies.get("access_token")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["id"] == user_id


@pytest.mark.asyncio
async def test_get_users_by_field(client: TestClient, override_db_dependency):
    registrer_user(client, override_db_dependency)
    client.post("/user", json=TEST_USER)
    assert client.cookies.get("access_token")
    search_data = {"email": TEST_USER["email"]}
    response = client.post("/user/user_by_field", json=search_data)
    assert client.cookies.get("access_token")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert isinstance(data[0], dict)
    assert data[0]["email"] == TEST_USER["email"]


@pytest.mark.asyncio
async def test_update_user(client: TestClient, override_db_dependency):
    registrer_user(client, override_db_dependency)
    create_response = client.post("/user", json=TEST_USER)
    assert client.cookies.get("access_token")
    user_id = create_response.json()["id"]
    update_data = TEST_USER_UPDATE
    update_data["id"] = user_id
    response = client.put(f"/user/{user_id}", json=update_data)
    assert client.cookies.get("access_token")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert data["email"] == TEST_USER_UPDATE["email"]


@pytest.mark.asyncio
async def test_update_user_error(client: TestClient, override_db_dependency):
    registrer_user(client, override_db_dependency)
    create_response = client.post("/user", json=TEST_USER)
    assert client.cookies.get("access_token")
    user_id = create_response.json()["id"]
    update_data = TEST_USER_UPDATE_ERR
    update_data["id"] = user_id
    response = client.put(f"/user/{user_id}", json=update_data)
    assert client.cookies.get("access_token")
    assert response.status_code == 400
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert "User could not be updated" in rsp["detail"]


@pytest.mark.asyncio
async def test_delete_user(client: TestClient, override_db_dependency):
    registrer_user(client, override_db_dependency)
    create_response = client.post("/user", json=TEST_USER)
    assert client.cookies.get("access_token")
    user_id = create_response.json()["id"]
    response = client.delete(f"/user/user/{user_id}")
    assert client.cookies.get("access_token")
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert rsp["email"] == TEST_USER["email"]
    assert response.status_code == 200
    response = client.get(f"/user/{user_id}")
    assert response.status_code == 404
    rsp = response.json()
    assert isinstance(rsp, dict)
    assert "User not found" in rsp["detail"]

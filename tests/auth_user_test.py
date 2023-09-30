import pytest
from fastapi.testclient import TestClient
from main import app
import random
id = random.randint(1, 1000000)


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as _client:
        yield _client

@pytest.fixture(scope="module")
def test_user():
    return {"username": str(id), "password": "string"}

def test_create_user(client: TestClient) -> None:
    response = client.post("/auth", data="{\"id\": \"" + str(id) + "\", \"username\": \"" + str(id) + "\", \"password\": \"string\", \"is_admin\": \"1\"}")
    assert "OK" in response.text
    
def test_create_token_and_login(client: TestClient, test_user):
    response = client.post("/auth/token", data=test_user)

    # Check the response status code and body to verify that the request was successful.
    assert response.status_code == 200
    assert response.json()["access_token"] is not None
    token = response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}" 

    }
    
    response = client.get("/check_admin", headers=headers)

    # Check the response status code and body to verify that the request was successful.
    assert response.status_code == 200

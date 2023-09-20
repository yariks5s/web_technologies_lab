import pytest
from fastapi.testclient import TestClient
from main import app
import random
id = random.randint(1, 1000000)

@pytest.fixture(scope="session")
def client():
    with TestClient(app) as _client:
        yield _client

def test_home(client: TestClient) -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "Example" in response.text

def tests_categories_creation(client: TestClient) -> None:
    response = client.post("/createJSON_categories/", content="{\"id\": \"" + str(id) + "\",\"name\": \"test_val\"}")
    assert response.status_code == 200

    response = client.get(f"/get_categories/{id}")
    assert response.status_code == 200
    assert "test_val" in response.text  # Test can be flaky due to possible repeats in id

def test_categories_deletion(client: TestClient) -> None:
    response = client.get(f"/delete_categories/{id}")
    assert response.status_code == 200
    assert "Deleting submitted successfully" in response.text

    response = client.get(f"/get_categories/{id}")
    assert response.status_code == 200
    assert not ("test_val"  in response.text) \
            and "Something went wrong" in response.text
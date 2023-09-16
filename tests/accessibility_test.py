from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/is_up")
    assert response.status_code == 200

def test_check_default_news():
    response = client.get("/get_news/1")
    assert response.status_code == 200

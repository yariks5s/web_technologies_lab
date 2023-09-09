def test_docker_base_image():
    assert "COPY requirements.txt ." in open("./Dockerfile").read()
    assert "RUN pip install --no-cache-dir -r requirements.txt" in open("./Dockerfile").read()
    assert "uvicorn main:app --host 0.0.0.0" in open("./docker-compose.yml").read()
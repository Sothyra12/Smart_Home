# app/tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/login", json={"username": "admin", "password": "secret"})
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}

def test_login_failure():
    response = client.post("/login", json={"username": "admin", "password": "wrong"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to SynHome API"}

def test_user_endpoint():
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    # Add more assertions based on your endpoint's response

def test_auth_endpoint():
    response = client.post("/api/v1/auth/login", json={"username": "test", "password": "test"})
    assert response.status_code == 200
    # Add more assertions based on your endpoint's response

def test_rooms_endpoint():
    response = client.get("/api/v1/rooms")
    assert response.status_code == 200
    # Add more assertions based on your endpoint's response

def test_devices_endpoint():
    response = client.get("/api/v1/devices")
    assert response.status_code == 200
    # Add more assertions based on your endpoint's response
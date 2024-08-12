# app/tests/test_main.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    response = client.post("/api/v1/auth/login", json={    
    "email": "ian2@example.com",
    "username": "ian2@example.com",
    "password": "mypassword"
        })
    assert response.status_code == 200
    assert response.json().keys() == {"access_token", "token_type", "user"}
    assert response.json()["token_type"] == "bearer"
    assert set(response.json()["user"].keys()) == {"username", "email", "user_id"}

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
    login_response = client.post("/api/v1/auth/login", json={    
        "email": "ian2@example.com",
        "username": "ian2@example.com",
        "password": "mypassword"
    })
   
    assert login_response.status_code == 200
    
    # Extract the access token from the login response
    access_token = login_response.json()["access_token"]
    
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/api/v1/rooms", headers=headers)
    
    assert response.status_code == 200
    # Add more assertions based on your endpoint's response

def test_devices_endpoint():
    login_response = client.post("/api/v1/auth/login", json={    
        "email": "ian2@example.com",
        "username": "ian2@example.com",
        "password": "mypassword"
    })
   
    assert login_response.status_code == 200
    
    # Extract the access token from the login response
    access_token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}

    response = client.get("/api/v1/devices", headers=headers)
    assert response.status_code == 200
    # Add more assertions based on your endpoint's response
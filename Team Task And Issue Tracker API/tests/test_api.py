def test_health_check(client):
    response = client.get("/health")
    
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy", "message": "The API is running"}
    
def test_create_api(client):
    payload = {
        "username": "amankhanal1960",
        "email": "amankhanal1960@gmail.com",
        "password": "amankhanal123"
    }
    response = client.post("/auth/register", json=payload)
    
    assert response.status_code == 201, response.json()
    data = response.json()
    assert data["username"] == "amankhanal1960"
    assert data["email"] == "amankhanal1960@gmail.com"

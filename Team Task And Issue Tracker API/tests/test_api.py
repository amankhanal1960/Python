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

def test_duplicate_api(client):
    payload = {
        "username": "amankhanal1960",
        "email": "amankhanal1960@gmail.com",
        "password": "amankhanal1234"
    }
    first_response = client.post("/auth/register", json=payload)
    
    assert first_response.status_code == 201, first_response.json()
    
    second_response = client.post("/auth/register", json=payload)
    assert second_response.status_code == 400
    
    assert second_response.json()["detail"] == "User with this email already exists"


def test_create_project(client):
    payload = {
        "name": "Amans Project",
        "description": "odsufberokuhsfpkjvhebfjklrgns",
        "owner_id": "32"
    }
    
    response = client.post("/project/", json=payload)
        
    assert response.status_code == 201, response.json()
    data = response.json()
    
    assert data["name"] == "Amans Project"
    assert data["description"] == "odsufberokuhsfpkjvhebfjklrgns"
    assert data["owner_id"] == "32"
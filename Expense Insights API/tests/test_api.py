def test_health_check(client):
    # Send a simulated GET call to the health route
    response = client.get("/health")
    
    # Check that the status code is exactly 200 OK
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "message": "API is running"}

def test_create_valid_transaction(client):
    payload = {
        "amount": "45.50",
        "category": "Dining Out",
        "type": "expense",
        "date": "2026-10-30",
        "note": "Dinner with team"
    }
    response = client.post("/transactions", json=payload)
    
    # Verify success rules
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "Dining Out"
    assert data["amount"] == "45.50"
    assert "id" in data  # Ensure the database generated a primary ID key

def test_create_invalid_negative_amount(client):
    payload = {
        "amount": "-10.00", # Should trigger our Pydantic gt=0 constraint bouncer!
        "category": "Invalid",
        "type": "expense",
        "date": "2026-10-30"
    }
    response = client.post("/transactions", json=payload)
    
    # Verify that the bouncer correctly locked out the invalid entry
    assert response.status_code == 422
    
def test_create_valid_budget(client):
    payload = {
        "category": "Food",
        "month": 12,
        "year": 2026,
        "budget_amount": "2000"
    }
    response = client.post("/budget", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "Food"
    assert data["month"] == 12
    assert data["year"] == 2026
    assert "id" in data
    
def test_create_invalid_budget(client):
    payload = {
        "category": "Food",
        "month": 209,
        "year": 2026,
        "budget_amount": "4000"
    }
    response = client.post("/budget", json=payload)
    assert response.status_code == 422

def test_get_transaction_by_category(client):
    payload = {
        "amount": "45.50",
        "category": "Dining Out",
        "type": "expense",
        "date": "2026-10-30",
        "note": "Dinner with team"
    }
    client.post("/transactions", json=payload)
    
    response = client.get("/transactions?category=Dining Out")
    print(response.json())
    
    assert response.status_code == 200
    assert len(response.json()) == 1
    
    
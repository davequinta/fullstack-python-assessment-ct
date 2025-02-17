from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

#Test creating a new product
def test_create_product():
    response = client.post("/products/", json={
        "name": "Test Product",
        "description": "This is a test product.",
        "price": 50.99,
        "stock": 100
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

#Test creating a product with an invalid price
def test_create_product_invalid_price():
    response = client.post("/products/", json={
        "name": "Invalid Product",
        "description": "Should fail due to invalid price.",
        "price": -10,
        "stock": 100
    })
    assert response.status_code == 422  # Validation error

#Test retrieving all products
def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)  # Should return a list

#Test retrieving a single product that exists
def test_get_product():
    response = client.get("/products/1")  # Assuming ID 1 exists
    assert response.status_code == 200
    assert "name" in response.json()

# Test retrieving a product that does not exist
def test_get_nonexistent_product():
    response = client.get("/products/9999")  # ID does not exist
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

#Test updating a product
def test_update_product():
    response = client.put("/products/1", json={
        "name": "Updated Product",
        "description": "Updated description.",
        "price": 99.99,
        "stock": 50
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"

#Test updating a product that does not exist
def test_update_nonexistent_product():
    response = client.put("/products/9999", json={
        "name": "Updated Name",
        "description": "Updated description.",
        "price": 99.99,
        "stock": 50
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

#Test deleting a product
def test_delete_product():
    response = client.delete("/products/1")  # Assuming ID 1 exists
    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted"

#Test deleting a product that does not exist
def test_delete_nonexistent_product():
    response = client.delete("/products/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

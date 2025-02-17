from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from app.main import app
from app.database import Base, get_db

#Use a persistent test database instead of in-memory
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Create a session-level test database that persists across tests
@pytest.fixture(scope="session")
def db_session():
    """Ensures the database schema is created before tests start."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

#Override FastAPI's `get_db()` dependency to use the test session
@pytest.fixture(scope="session")
def client(db_session):
    """Overrides FastAPI's database dependency for testing."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

#Test creating a new product
def test_create_product(client):
    response = client.post("/products/", json={
        "name": "Test Product",
        "description": "This is a test product.",
        "price": 50.99,
        "stock": 100
    })
    assert response.status_code == 201
    assert response.json()["name"] == "Test Product"
    assert "id" in response.json()

#Test creating a product with an invalid price
def test_create_product_invalid_price(client):
    response = client.post("/products/", json={
        "name": "Invalid Product",
        "description": "Should fail due to invalid price.",
        "price": -10,
        "stock": 100
    })
    assert response.status_code == 422  #Validation error

#Test retrieving all products
def test_get_products(client):
    response = client.get("/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

#Test retrieving a single product that exists
def test_get_product(client):
    product = client.post("/products/", json={
        "name": "Test Product",
        "description": "This is a test product.",
        "price": 50.99,
        "stock": 100
    }).json()

    response = client.get(f"/products/{product['id']}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Product"

#Test retrieving a product that does not exist
def test_get_nonexistent_product(client):
    response = client.get("/products/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

#Test updating a product
def test_update_product(client):
    product = client.post("/products/", json={
        "name": "Test Product",
        "description": "This is a test product.",
        "price": 50.99,
        "stock": 100
    }).json()

    response = client.put(f"/products/{product['id']}", json={
        "name": "Updated Product",
        "description": "Updated description.",
        "price": 99.99,
        "stock": 50
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"

#Test updating a product that does not exist
def test_update_nonexistent_product(client):
    response = client.put("/products/9999", json={
        "name": "Updated Name",
        "description": "Updated description.",
        "price": 99.99,
        "stock": 50
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

#Test deleting a product
def test_delete_product(client):
    product = client.post("/products/", json={
        "name": "Test Product",
        "description": "This is a test product.",
        "price": 50.99,
        "stock": 100
    }).json()

    response = client.delete(f"/products/{product['id']}")
    assert response.status_code == 204

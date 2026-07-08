from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_create_item():
    response = client.post("/items/", json={"name": "Test Item", "price": 9.99})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["price"] == 9.99
    assert "id" in data


def test_read_item():
    response = client.post("/items/", json={"name": "Read Test", "price": 5.0})
    item_id = response.json()["id"]

    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Read Test"


def test_read_item_not_found():
    response = client.get("/items/99999")
    assert response.status_code == 200
    assert response.json() == {"error": "Item not found"}

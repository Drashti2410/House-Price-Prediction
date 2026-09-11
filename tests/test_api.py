from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

VALID_HOUSE = {
    "area": 3500, "bedrooms": 3, "bathrooms": 2, "stories": 2, "parking": 1,
    "mainroad": "yes", "guestroom": "no", "basement": "yes",
    "hotwaterheating": "no", "airconditioning": "yes", "prefarea": "yes",
    "furnishingstatus": "semi-furnished"
}

def test_health():
    assert client.get("/health").status_code == 200

def test_predict_valid():
    r = client.post("/predict", json=VALID_HOUSE)
    assert r.status_code == 200
    assert r.json()["predicted_price"] > 0

def test_predict_invalid_bedrooms():
    bad = VALID_HOUSE.copy()
    bad["bedrooms"] = 99
    r = client.post("/predict", json=bad)
    assert r.status_code == 422

def test_listings_filter():
    r = client.get("/listings?min_price=5000000")
    assert r.status_code == 200

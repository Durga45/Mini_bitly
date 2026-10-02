from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_shorten_url():
    response = client.post("/shorten", json={"original_url": "https://github.com"})
    assert response.status_code == 200
    data = response.json()
    assert "short_code" in data
    assert data["original_url"] == "https://github.com"

def test_root_redirect_404():
    response = client.get("/invalidcode123")
    assert response.status_code == 404
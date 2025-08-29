
import pytest
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_shaming(client):
    data = {
        "Version": "0.2",
        "Title": "Sigo cometiendo los mismos errores",
        "Texts": [
            {"Text": "Ignorar consejos es lo mío", "ID": "t1"},
            {"Text": "Siempre llego tarde", "ID": "t2"}
        ],
        "Buttons": [
            {"Label": "Promesas que no cumplo", "ID": "b1"}
        ],
        "Path": "test/path"
    }
    response = client.post("/shaming", json=data)
    assert response.status_code == 200
    assert "Version" in response.json
    assert response.json["Version"] == "0.2"
    assert "Title" in response.json
    assert "ShamingInstances" in response.json
    assert "Path" in response.json

def test_urgency(client):
    data = {
        "Version": "0.1",
        "tokens": [
            {"text": "¡Solo quedan 2 unidades!", "path": "test/path"},
            {"text": "Oferta termina pronto", "path": "test/path"}
        ]
    }
    response = client.post("/urgency", json=data)
    assert response.status_code == 200
    assert "UrgencyInstances" in response.json
    assert response.json["Version"] == "0.1"
    assert isinstance(response.json["UrgencyInstances"], list)

def test_scarcity(client):
    data = {
        "Version": "0.1",
        "tokens": [
            {"text": "Últimas 3 unidades disponibles", "path": "test/path"},
            {"text": "Solo quedan 1", "path": "test/path"}
        ]
    }
    response = client.post("/scarcity", json=data)
    assert response.status_code == 200
    assert "ScarcityInstances" in response.json
    assert response.json["Version"] == "0.1"
    assert isinstance(response.json["ScarcityInstances"], list)

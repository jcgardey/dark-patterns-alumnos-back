
import pytest
import json
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_shaming(client):
    # Leer data desde ejemplos.json
    with open("ejemplos.json", encoding="utf-8") as f:
        data = json.load(f)
    # Adaptar al schema esperado
    data_schema = {
        "Version": data["Version"],
        "Title": data["Title"],
        "Texts": data["Texts"],
        "Buttons": data["Buttons"],
        "Path": data["Path"]
    }
    response = client.post("/shaming", json=data_schema)
    assert response.status_code == 200
    assert "Version" in response.json
    assert response.json["Version"] == data["Version"]
    assert "Title" in response.json
    assert "ShamingInstances" in response.json
    assert "Path" in response.json

    # Test: los IDs que empiezan con 'n' no son shaming
    for instance in response.json["ShamingInstances"]:
        if instance["ID"].startswith("n"):
            assert not instance["HasShaming"], f"ID {instance['ID']} no debe ser shaming"

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

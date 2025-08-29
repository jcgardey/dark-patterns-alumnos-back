

import pytest
import json
from app import app
from src.urgency.types import UrgencyRequestSchema, UrgencyResponseSchema

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_shaming(client):
    with open("ejemplos.json", encoding="utf-8") as f:
        data = json.load(f)
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

    for instance in response.json["ShamingInstances"]:
        if instance["ID"].startswith("n"):
            assert not instance["HasShaming"], f"ID {instance['ID']} no debe ser shaming"

def test_urgency(client):
    with open("ejemplos_urgency.json", encoding="utf-8") as f:
        data = json.load(f)

    schema = UrgencyRequestSchema()
    valid_data = schema.load(data)
    response = client.post("/urgency", json=valid_data)
    assert response.status_code == 200

    response_schema = UrgencyResponseSchema()
    resp = response_schema.load(response.json)

    assert "UrgencyInstances" in resp
    assert resp["Version"] == valid_data["Version"]
    assert isinstance(resp["UrgencyInstances"], list)

    detected_by_id = {}
    for instance in resp["UrgencyInstances"]:
        for token in valid_data["tokens"]:
            if instance["text"].strip() == token["text"].strip() and instance["path"] == token["path"]:
                detected_by_id[token.get("id")] = True

    for token in valid_data["tokens"]:
        if token.get("id", "").startswith("e"):
            assert token["id"] in detected_by_id, f"ID {token['id']} debería ser detectado como urgencia"

    for token in valid_data["tokens"]:
        if token.get("id", "").startswith("n"):
            assert token["id"] not in detected_by_id, f"ID {token['id']} no debe ser urgencia"



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

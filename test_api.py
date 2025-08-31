import pytest
import json
from app import app
from src.scarcity.types import ScarcityRequestSchema
from src.urgency.types import UrgencyRequestSchema, UrgencyResponseSchema
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

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
    print(resp)
    assert "urgency_instances" in resp
    assert resp["version"] == valid_data["version"]
    assert isinstance(resp["urgency_instances"], list)

    detected_by_id = {}
    for instance in resp["urgency_instances"]:
        if "id" in instance:
            detected_by_id[instance["id"]] = instance["has_urgency"]

    for text_obj in valid_data["texts"]:
        print(text_obj)
        id_ = text_obj.get("id")
        if id_ is None:
            continue
        if id_.startswith("e"):
            assert detected_by_id.get(id_) is True, f"ID {id_} debería ser detectado como urgencia"
        if id_.startswith("n"):
            assert detected_by_id.get(id_) is False or id_ not in detected_by_id, f"ID {id_} no debe ser urgencia"



def test_scarcity(client):
    with open("ejemplos_scarcity.json", encoding="utf-8") as f:
        data = json.load(f)
    data = ScarcityRequestSchema().load(data)
    response = client.post("/scarcity", json=data)
    assert response.status_code == 200
    assert "instances" in response.json
    assert response.json["version"] == "1.0"

    instances = response.json["instances"]
    e_ids = [inst for inst in instances if inst.get("id", "").startswith("e")]
    n_ids = [inst for inst in instances if inst.get("id", "").startswith("n")]

    for inst in e_ids:
        assert inst.get("has_scarcity") is True, f"ID {inst.get('id')} debería ser detectado como scarcity"

    for inst in n_ids:
        assert inst.get("has_scarcity") is False, f"ID {inst.get('id')} no debe ser scarcity"
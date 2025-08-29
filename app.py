from flask import Flask, request
from flask_cors import CORS
from src.shaming.shaming import check_text_shaming, check_text_shaming_nopath

from src.urgency.urgency import check_text_urgency
from src.scarcity.scarcity import check_text_scarcity
from src.urgency.types import UrgencyRequestSchema, UrgencyResponseSchema
from src.scarcity.types import ScarcityRequestSchema, ScarcityResponseSchema

from src.shaming.types import ShamingSchema, ShamingResponse

app = Flask(__name__)
CORS(app)

@app.post("/scarcity")
def detect_scarcity():
    """
    Detecta patrones de escasez en los datos recibidos mediante una solicitud POST.
    Utiliza schemas estandarizados para validar y serializar la entrada y salida.
    """
    json_data = request.get_json()
    schema = ScarcityRequestSchema()
    data = schema.load(json_data)
    scarcity_instances = []
    for token in data["tokens"]:
        scarcity_instances.extend(check_text_scarcity(token["text"], token["path"]))
    response_schema = ScarcityResponseSchema()
    response = {
        "Version": data["Version"],
        "ScarcityInstances": scarcity_instances
    }
    return response_schema.dump(response)


@app.post("/shaming")
def detect_shaming():
    """
    Detecta patrones de 'shaming' en los datos recibidos mediante una solicitud POST.

    Esta función maneja la ruta '/shaming' y procesa los datos JSON enviados en la solicitud.
    Dependiendo de la versión especificada en el JSON, utiliza diferentes métodos para analizar los textos:

    - Si la versión es distinta de "0.2", itera sobre los tokens recibidos y utiliza la función `check_text_shaming`
        para detectar patrones de shaming en cada texto, devolviendo una lista de resultados.
    - Si la versión es "0.2", valida y deserializa los datos usando `ShamingSchema`, luego procesa los textos con
        `check_text_shaming_nopath` y devuelve la respuesta serializada con `ShamingResponse`.

    Returns:
        list o dict: Resultados del análisis de shaming, dependiendo de la versión del esquema recibido.
    """
    json_data = request.get_json()
    if json_data.get("Version", "0.1") != "0.2":
        sentences = []
        tokens = request.get_json().get("tokens")
        for token in tokens:
            sentences.extend(check_text_shaming(token["text"], token["path"]))
        return sentences
    else:
        schema = ShamingSchema()
        data = schema.load(json_data)
        response_schema = ShamingResponse()
        return response_schema.dump(check_text_shaming_nopath(data))



@app.post("/urgency")
def detect_urgency():
    """
    Detecta patrones de urgencia en los datos recibidos mediante una solicitud POST.
    Utiliza schemas estandarizados para validar y serializar la entrada y salida.
    """
    json_data = request.get_json()
    schema = UrgencyRequestSchema()
    data = schema.load(json_data)
    urgency_instances = []
    for token in data["tokens"]:
        # Chequeo de urgencia (genuina)
        urgency_instances.extend(check_text_urgency(token["text"], token["path"]))
    response_schema = UrgencyResponseSchema()
    response = {
        "Version": data["Version"],
        "UrgencyInstances": urgency_instances
    }
    return response_schema.dump(response)

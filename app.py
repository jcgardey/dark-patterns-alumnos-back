from flask import Flask, request
from flask_cors import CORS
from src.shaming.shaming import check_text_shaming, check_text_shaming_nopath

from src.urgency.urgency import check_text_urgency
from src.scarcity.scarcity import check_text_scarcity, check_text_scarcity_schema
from src.urgency.types import UrgencyRequestSchema, UrgencyResponseSchema
from src.scarcity.types import ScarcityRequestSchema, ScarcityResponseSchema
from src.urgency.urgency import check_text_urgency_schema

from src.shaming.types import ShamingSchema, ShamingResponse

app = Flask(__name__)
CORS(app)

@app.post("/scarcity")
def detect_scarcity():
    """
    Detecta patrones de escasez en los datos recibidos mediante una solicitud POST.
    Utiliza schemas estandarizados para validar y serializar la entrada y salida.
    """
    json_data = ScarcityRequestSchema().load(request.get_json())
    return check_text_scarcity_schema(json_data)


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
    json_data = UrgencyRequestSchema().load(request.get_json())
    return check_text_urgency_schema(json_data)

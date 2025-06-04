from flask import Flask, request
from flask_cors import CORS
from src.shaming.shaming import check_text_shaming
from src.urgency.urgency import check_text_urgency

app = Flask(__name__)
CORS(app)


@app.post("/shaming")
def detect_shaming():
    """
    Detecta patrones de 'Confirm Shaming' en un conjunto de textos proporcionados.

    Esta función recibe una solicitud POST con un JSON que contiene una lista de tokens.
    Cada token incluye un texto y una ruta asociada. La función analiza cada texto en busca
    de patrones de 'Confirm Shaming' utilizando la función `check_text_shaming` y devuelve una lista
    de oraciones que contienen dichos patrones.

    Returns:
        sentences: Una lista de diccionarios, donde cada diccionario contiene:
        - "text" (str): La oración que contiene el patrón identificado.
        - "path" (str): La ruta proporcionada como contexto.
        - "pattern" (str): El nombre del patrón identificado ("SHAMING"). lista de oraciones que contienen patrones de 'Confirm Shaming'.

    Ejemplo de entrada esperada:
        {
            "tokens": [
                {"text": "Ejemplo de texto", "path": "/ruta/del/archivo"}
            ]
        }
    """
    sentences = []
    tokens = request.get_json().get("tokens")
    for token in tokens:
        sentences.extend(check_text_shaming(token["text"], token["path"]))
    return sentences


@app.post("/urgency")
def detect_urgency():
    """
    Detecta patrones de "Fake Urgency" en un conjunto de textos proporcionados.

    Esta función recibe una solicitud POST con un JSON que contiene una lista de tokens.
    Cada token incluye un texto y una ruta asociada. La función analiza cada texto
    para identificar patrones de "Fake Urgency" utilizando la función `check_text_urgency`.

    Returns:
        list: Una lista de oraciones que contienen patrones de "Fake Urgency" detectados.

    Request JSON:
        {
            "tokens": [
                {
                    "text": "Texto a analizar",
                    "path": "Ruta asociada al texto"
                },
                ...
            ]
        }
    """
    sentences = []
    tokens = request.get_json().get("tokens")
    for token in tokens:
        sentences.extend(check_text_urgency(token["text"], token["path"]))
    return sentences

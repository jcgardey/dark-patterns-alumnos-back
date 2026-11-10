from config import NLP
from spacy.matcher import Matcher
from src.scarcity.types import ScarcityResponseSchema

scarcity_matcher = Matcher(NLP.vocab)
scarcity_patterns = [
    # Oraciones del tipo "Últimas 3 unidades" o "ultimo disponible"
    [
        {"LOWER": {"FUZZY": {"IN": ["ultima", "ultimo"]}}},
        {"TEXT": {"REGEX": r"^\d*"}, "OP": "?"},
        {"LOWER": {"FUZZY": {"IN": ["unidade", "disponible"]}}},
    ],
    # Oraciones del tipo "Solo quedan 3"
    [
        {"LOWER": {"FUZZY1": "solo"}},
        {"LOWER": {"FUZZY1": "queda"}},
        {"TEXT": {"REGEX": r"^\d+"}},
    ],
    # Oraciones del tipo "Últimas unidades disponibles"
    [
        {
            "LEMMA": {"IN": ["último", "ultimo"]},
            "POS": "ADJ",
        },
        {"IS_DIGIT": True, "OP": "?"},
        {"POS": "NOUN"},
        {"POS": "ADJ", "OP": "?"},
    ],
    # Oraciones del tipo "¡Aprovecha! Quedan pocas unidades"
    [
        {"POS": "PUNCT", "OP": "*"},
        {
            "LEMMA": {"IN": ["quedar", "restar"]},
            "POS": "VERB",
        },
        {
            "LEMMA": {"IN": ["poco", "escaso", "limitado"]},
            "POS": {"IN": ["DET", "ADJ"]},
        },
        {
            "LEMMA": {"IN": ["unidad", "existencia", "articulo", "plaza"]},
            "POS": "NOUN",
        },
        {"POS": "PUNCT", "OP": "*"},
    ],
    [
        {"POS": "PUNCT", "OP": "*"},
        {
            "LEMMA": {
                "IN": ["comprar", "compra", "adquirir", "pedir", "ordenar", "haz"]
            },
            "POS": {"IN": ["VERB", "NOUN"]},
        },
        {"LEMMA": {"IN": ["ya", "ahora"]}, "POS": "ADV", "OP": "?"},
        {"LEMMA": "mismo", "POS": "ADJ", "OP": "?"},
        {"LEMMA": {"IN": ["antes", "previo"]}, "POS": "ADV"},
        {"LEMMA": "de", "POS": "ADP"},
        {"LEMMA": "que", "POS": "SCONJ"},
        {"LEMMA": "él", "POS": "PRON", "OP": "?"},
        {"LEMMA": {"IN": ["acabar", "terminar", "agotar", "acabar_se"]}, "POS": "VERB"},
        {"POS": "PUNCT", "OP": "*"},
    ],
    [
        {"IS_PUNCT": True, "OP": "*"},
        {"LOWER": {"REGEX": "s[oó]lo"}, "OP": "?"},  # Solo / Sólo (opcional)
        {"LIKE_NUM": True},  # 3 / tres
        {
            "LEMMA": {
                "IN": [
                    "unidad",
                    "pieza",
                    "artículo",
                    "articulo",
                    "existencia",
                    "producto",
                    "plaza",
                    "stock",
                ]
            },
            "POS": "NOUN",
        },
        {
            "POS": "ADJ",
            "LEMMA": {
                "IN": ["restante", "disponible", "limitado", "último", "ultimo", "poco"]
            },
            "OP": "?",  # restantes / disponibles (opcional)
        },
        {"IS_PUNCT": True, "OP": "*"},
    ],
    # Solo 3 restantes unidades (orden adjetivo-nombre, por si viene mal redactado)
    [
        {"IS_PUNCT": True, "OP": "*"},
        {"LOWER": {"REGEX": "s[oó]lo"}, "OP": "?"},
        {"LIKE_NUM": True},
        {
            "POS": "ADJ",
            "LEMMA": {
                "IN": ["restante", "disponible", "limitado", "último", "ultimo", "poco"]
            },
        },
        {
            "LEMMA": {
                "IN": [
                    "unidad",
                    "pieza",
                    "artículo",
                    "articulo",
                    "existencia",
                    "producto",
                    "plaza",
                    "stock",
                ]
            },
            "POS": "NOUN",
        },
        {"IS_PUNCT": True, "OP": "*"},
    ],
    # Solo 3 uds restantes!  /  Solo 3 u. disponibles
    [
        {"IS_PUNCT": True, "OP": "*"},
        {"LOWER": {"REGEX": "s[oó]lo"}, "OP": "?"},
        {"LIKE_NUM": True},
        {"LOWER": {"IN": ["u", "u.", "ud", "uds"]}},  # abreviaturas de unidades
        {
            "POS": "ADJ",
            "LEMMA": {
                "IN": ["restante", "disponible", "limitado", "último", "ultimo", "poco"]
            },
            "OP": "?",
        },
        {"IS_PUNCT": True, "OP": "*"},
    ],
    # 3 unidades en stock / 3 unidades disponibles (sin "Solo")
    [
        {"IS_PUNCT": True, "OP": "*"},
        {"LIKE_NUM": True},
        {
            "LEMMA": {
                "IN": [
                    "unidad",
                    "pieza",
                    "artículo",
                    "articulo",
                    "existencia",
                    "producto",
                    "plaza",
                    "stock",
                ]
            },
            "POS": "NOUN",
        },
        {"LOWER": "en", "OP": "?"},
        {"LOWER": "stock", "OP": "?"},
        {
            "POS": "ADJ",
            "LEMMA": {
                "IN": ["restante", "disponible", "limitado", "último", "ultimo", "poco"]
            },
            "OP": "?",
        },
        {"IS_PUNCT": True, "OP": "*"},
    ],
    # Solo 3 restantes! (sin el sustantivo, frase cortada)
    [
        {"IS_PUNCT": True, "OP": "*"},
        {"LOWER": {"REGEX": "s[oó]lo"}},
        {"LIKE_NUM": True},
        {
            "POS": "ADJ",
            "LEMMA": {
                "IN": ["restante", "disponible", "limitado", "último", "ultimo", "poco"]
            },
        },
        {"IS_PUNCT": True, "OP": "*"},
    ],
    # Caso boton temu
    [   # Caso estricto de ¡Los Ultimos! o simil
        {"ORTH": {"IN": ["¡", "!"]}, "OP": "?"},            # Signo de apertura opcional
        {"LOWER": {"IN": ["los", "las"]}},                   # "los" o "las"
        {"LOWER": {"IN": ["últimos", "ultimos", "últimas", "ultimas"]}}, # Con o sin tilde
        {"ORTH": {"IN": ["!", "!!", "!!!"]}, "OP": "+"}      # Al menos un signo de exclamación al final
    ],
    # Caso Contextual "Los últimos" + contexto de compra/carrito en la misma frase/oración
    [
        {"ORTH": "¡", "OP": "?"},                           # '¡' Opcional
        {"LOWER": {"IN": ["los", "las"]}},                   # 'los' / 'las'
        {"LOWER": {"IN": ["últimos", "ultimos", "últimas", "ultimas"]}},
        {"ORTH": "!", "OP": "*"},                           # '!' Opcional/múltiple
        
        # Permite entre 0 y 6 tokens de cualquier tipo entre medio 
        # (cubre: "!", "¡", "Agregar", "al", etc.)
        {"OP": "{0,6}"},                                    
        
        # Términos clave del entorno de compra
        {"LOWER": {"IN": ["carrito", "bolsa", "cesta", "comprar", "agregar", "añadir"]}}
    ]
]
scarcity_matcher.add("fake_scarcity", scarcity_patterns)


def check_text_scarcity(text):
    """
    Analiza el texto para detectar patrones de escasez y devuelve coincidencias encontradas.

    Parámetros:
        text (str): El texto que se desea analizar en busca de patrones de escasez.

    Retorna:
        list[dict]: Una lista de diccionarios, cada uno representando una coincidencia encontrada.
            Cada diccionario contiene:
                - "text" (str): El fragmento de texto que coincide con un patrón de escasez.
                - "pattern" (str): El nombre del patrón de escasez detectado.

    Notas sobre variables internas:
        - doc: Objeto procesado por el modelo NLP a partir del texto de entrada.
        - token: Cada palabra o símbolo individual en el texto, con atributos como lemma, parte de la oración, etc.
        - matches: Coincidencias encontradas por scarcity_matcher en el texto procesado.
        - span: Fragmento del texto correspondiente a una coincidencia.
    """
    doc = NLP(text)
    matches = scarcity_matcher(doc)
    results = []
    for match_id, start, end in matches:
        span = doc[start:end]
        results.append({"text": span.text, "pattern": NLP.vocab.strings[match_id]})
    return results


def check_text_scarcity_schema(data):
    """
    Recibe un dict validado por ScarcityRequestSchema
    y devuelve la respuesta serializada por ScarcityResponseSchema.
    Cada instancia indica si el texto tiene escasez (has_scarcity).
    """
    texts_input = data.get("texts", [])
    if not texts_input:
        return ScarcityResponseSchema().dump({"version": data.get("version", "1.0"), "instances": []})

    text_strings = [item["text"] for item in texts_input]
    docs = list(NLP.pipe(text_strings, batch_size=50))

    instances = []
    for item, doc in zip(texts_input, docs):
        text = item["text"]
        path = item.get("path")
        id_ = item.get("id")
        matches = scarcity_matcher(doc)
        instance = {"text": text, "path": path, "has_scarcity": bool(matches)}
        if id_ is not None:
            instance["id"] = id_
        instances.append(instance)

    response_schema = ScarcityResponseSchema()
    response = {"version": data.get("version", "1.0"), "instances": instances}
    return response_schema.dump(response)

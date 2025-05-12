from config import NLP
from spacy.matcher import Matcher


# Fake Scarcity matcher
fake_scarcity_matcher = Matcher(NLP.vocab)
fake_scarcity_patterns = [
    # Oraciones del tipo "Últimas 3 unidades" o "ultimo disponible"
    [
        {"LOWER": {"FUZZY": {"IN": ["ultima", "ultimo"]}}},
        {"TEXT": {"REGEX": "^\d*"}, "OP": "?"},
        {"LOWER": {"FUZZY": {"IN": ["unidade", "disponible"]}}},
    ],
    # Oraciones del tipo "Solo quedan 3"
    [
        {"LOWER": {"FUZZY1": "solo"}},
        {"LOWER": {"FUZZY1": "queda"}},
        {"TEXT": {"REGEX": "^\d+"}},
    ],
]
fake_scarcity_matcher.add("fake_scarcity", fake_scarcity_patterns)


def check_text_urgency(text, path):
    """
    Analiza un texto para detectar patrones de urgencia y devuelve las oraciones que coinciden.
    Esta función utiliza un modelo de procesamiento de lenguaje natural (NLP) para identificar 
    coincidencias con patrones de escasez falsa en el texto proporcionado. Si se encuentran 
    coincidencias, se devuelve una lista de oraciones relevantes junto con información adicional.
    Args:
        text (str): El texto que se analizará en busca de patrones de urgencia.
        path (str): La ruta asociada al texto, utilizada para proporcionar contexto en los resultados.
    Returns:
        list: Una lista de diccionarios, donde cada diccionario contiene:
            - "text" (str): La oración que contiene el patrón de urgencia.
            - "path" (str): La ruta asociada al texto analizado.
            - "pattern" (str): El tipo de patrón detectado (en este caso, "URGENCY").
    """
    doc = NLP(text)
    fake_scarcity_matches = fake_scarcity_matcher(doc, as_spans=True)

    sentences = []
    if fake_scarcity_matches:
        print(fake_scarcity_matches[0].sent.text, fake_scarcity_matches[0].text)
        sentences.append(
            {
                "text": fake_scarcity_matches[0].sent.text,
                "path": path,
                "pattern": "URGENCY",
            }
        )
    return sentences

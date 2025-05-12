from config import NLP
from spacy.matcher import Matcher

# lista de palabras que no deberían considerarse en el matching de Confirmshaming
SHAMING_EXCEPTIONS = ["inicio"]

# Confirmshaming matcher
first_person_matcher = Matcher(NLP.vocab)
first_person_verb_pattern = [
    # Verbos en primera persona
    [{"POS": "VERB", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}}],
    # Oraciones del tipo "Soy una mala persona"
    [
        {
            "DEP": "cop",
            "POS": "AUX",
            "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]},
        }
    ],
    # "Me gusta..."
    [
        {"POS": "PRON", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}},
        {"POS": "VERB"},
    ],
    # "Me voy a hacer..."
    [
        {
            "DEP": "aux",
            "POS": "AUX",
            "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]},
        },
        {"DEP": "mark", "POS": "ADP"},
        {"POS": "VERB"},
    ],
    # Nuevos patrones para ironía/sarcasmo
    # "Prefiero no saber nada útil"
    [
        {"LEMMA": "preferir", "POS": "VERB"},
        {"LOWER": "no"},
        {"POS": "VERB"},
    ],
    # "¿Quién necesita aprender...?"
    [
        {"LOWER": "quién"},
        {"LEMMA": "necesitar", "POS": "VERB"},
    ],
    # "¿Por qué habría de...?"
    [
        {"LOWER": "por"},
        {"LOWER": "qué"},
        {"LEMMA": "haber", "POS": "AUX"},
        {"LOWER": "de"},
        {"POS": "VERB"},
    ],
    # "Ignorar soluciones fáciles es mi especialidad"
    [
        {"LEMMA": "ignorar", "POS": "VERB"},
        {"POS": "NOUN", "OP": "+"},
        {"LEMMA": "ser", "POS": "AUX"},
        {"LOWER": "mi"},
        {"POS": "NOUN"},
    ],
    # "Seguir haciendo las cosas mal es lo mío"
    [
        {"LEMMA": "seguir", "POS": "VERB"},
        {"POS": "VERB"},
        {"POS": "DET", "OP": "?"},
        {"POS": "NOUN", "OP": "*"},
        {"LEMMA": "ser", "POS": "AUX"},
        {"LOWER": "lo"},
        {"LOWER": "mío"},
    ],
    # "vivir confundido es mi estilo"
    [
        {"LEMMA": "vivir", "POS": "VERB"},
        {"POS": "ADJ", "OP": "?"},
        {"LEMMA": "ser", "POS": "AUX"},
        {"LOWER": "mi"},
        {"POS": "NOUN"},
    ],
]

first_person_matcher.add("first_person", first_person_verb_pattern)


def check_text_shaming(text, path):
    """
    Analiza un texto para identificar patrones de "shaming" (avergonzar)
    basados en el uso de verbos en primera persona y devuelve una lista
    de oraciones que coinciden con el patrón.
    Args:
        text (str): El texto que se analizará en busca de patrones de "shaming".
        path (str): La ruta del archivo o contexto asociado al texto analizado.
    Returns:
        list: Una lista de diccionarios, donde cada diccionario contiene:
            - "text" (str): La oración que contiene el patrón identificado.
            - "path" (str): La ruta proporcionada como contexto.
            - "pattern" (str): El nombre del patrón identificado ("SHAMING").
        Si no se encuentran coincidencias, devuelve una lista vacía.
    """
    doc = NLP(text)
    # Match first person verbs
    first_person_matches = first_person_matcher(doc, as_spans=True)

    sentences = []
    if first_person_matches:
        # Check for exceptions
        if first_person_matches[0].text.lower() in SHAMING_EXCEPTIONS:
            return []
        print(first_person_matches[0].sent.text, first_person_matches[0].text)
        sentences.append(
            {
                "text": first_person_matches[0].sent.text,
                "path": path,
                "pattern": "SHAMING",
            }
        )
    return sentences

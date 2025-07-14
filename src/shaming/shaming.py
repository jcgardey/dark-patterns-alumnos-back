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


def is_an_exception(text):
    """
    Check if the text is in the list of exceptions.
    Args:
        text (str): The text to check.
    Returns:
        bool: True if the text is an exception, False otherwise.
    """
    return text.lower() in SHAMING_EXCEPTIONS


def check_shaming_in_text(text):
    doc = NLP(text)
    matches = first_person_matcher(doc, as_spans=True)
    if not matches:
        return False
    if is_an_exception(matches[0].text):
        return False
    return True


def check_text_shaming_nopath(data):
    """
    Analyzes the provided data for instances of shaming language in titles, texts, and button labels.
    Args:
        data (dict): A dictionary containing the following keys:
            - "Path" (str): The path associated with the data.
            - "Title" (str): The title text to check for shaming.
            - "Texts" (list of dict): Each dict contains:
                - "Text" (str): The text to check.
                - "ID" (str): The identifier for the text.
            - "Buttons" (list of dict): Each dict contains:
                - "Label" (str): The button label to check.
                - "ID" (str): The identifier for the button.
    Returns:
        dict: A dictionary with the following structure:
            - "Version" (str): The version of the response format.
            - "Title" (dict): Information about the title, including:
                - The title text.
                - "HasShaming" (bool): Whether shaming language was detected in the title.
                - "ID" (str): The identifier "Title".
            - "ShamingInstances" (list): List of dicts for each text/button label, each containing:
                - "Text" (str): The text or label checked.
                - "HasShaming" (bool): Whether shaming language was detected.
                - "ID" (str): The identifier for the text/button.
            - "Path" (str): The path from the input data.
    Note:
        Requires the function `check_shaming_in_text` to be defined elsewhere, which determines if a given text contains shaming language.
    """
    response = dict()
    response["Version"] = "0.2"
    response["ShamingInstances"] = []
    response["Path"] = data["Path"]

    if check_shaming_in_text(data["Title"]):
        response["Title"] = {"Text": data["Title"], "HasShaming": True, "ID": "Title"}
    else:
        response["Title"] = {"Text": data["Title"], "HasShaming": False, "ID": "Title"}

    for text in data["Texts"]:
        if check_shaming_in_text(text["Text"]):
            response["ShamingInstances"].append(
                {
                    "Text": text["Text"],
                    "HasShaming": True,
                    "ID": text["ID"],
                }
            )
        else:
            response["ShamingInstances"].append(
                {
                    "Text": text["Text"],
                    "HasShaming": False,
                    "ID": text["ID"],
                }
            )

    for button in data["Buttons"]:
        if check_shaming_in_text(button["Label"]):
            response["ShamingInstances"].append(
                {
                    "Text": button["Label"],
                    "HasShaming": True,
                    "ID": button["ID"],
                }
            )
        else:
            response["ShamingInstances"].append(
                {
                    "Text": button["Label"],
                    "HasShaming": False,
                    "ID": button["ID"],
                }
            )
    return response

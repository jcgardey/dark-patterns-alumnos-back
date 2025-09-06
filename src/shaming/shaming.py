from config import NLP
from spacy.matcher import Matcher

matcher = Matcher(NLP.vocab)

SHAMING_EXCEPTIONS = ["inicio"]
NEGATIVE_TERMS = {
    "verbos": ["ignorar", "mentir", "criticar", "procrastinar", "romper reglas", "cometer errores",
               "desobedecer", "manipular", "vengar", "envidiar",
    ],
    "adjetivos": ["desordenado", "egoísta", "sarcástico", "impuntual", "hiriente", "arrogante",
                  "grosero", "malhumorado", "perezoso", "despreocupado", "irritable", "intolerante",
                  "rudo", "desconsiderado", "cínico", "descuidado", "apático", "negligente",
                  "insensible", "deshonesto", "desagradable", "celoso", "resentido", "irresponsable",
                  "negativo", "ignorante"
    ],
    "sustantivos": ["bromas pesadas", "egoísmo", "irresponsabilidad", "deslealtad",
                    "bullying", "injusticia", "impaciencia",
    ],
    "frases_compuestas": ["promesas que no cumplo", "hacer caso omiso", "hacer lo mínimo posible",
        "seguir cometiendo los mismos errores", "seguir evitando responsabilidades", "seguir ignorando consejos",
        "seguir ignorando soluciones fáciles", "a último momento"
    ]
}
ALL_NEGATIVE_TERMS = (
    NEGATIVE_TERMS["verbos"] +
    NEGATIVE_TERMS["adjetivos"] +
    NEGATIVE_TERMS["sustantivos"] +
    NEGATIVE_TERMS["frases_compuestas"]
)

# --- Primera persona ---
matcher.add("FP_VERB", [
    [{"POS": "VERB", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}}],
])

matcher.add("FP_COPULA", [
    [{"DEP": "cop", "POS": "AUX", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}}],
])

matcher.add("FP_ME_VERB", [
    [{"POS": "PRON", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}}, {"POS": "VERB"}],
])

# --- Perífrasis ---
matcher.add("FP_PERIFRASIS_VOY_A", [
    [
        {"DEP": "aux", "POS": "AUX", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}},
        {"DEP": "mark", "POS": "ADP"},
        {"POS": "VERB"},
    ]
])

# Ser desordenado es lo mío
matcher.add("FP_ES_LO_MIO", [
    [
        {"LEMMA": {"IN": ["seguir", "ignorar", "ser", "hacer"]}, "POS": {"IN": ["VERB", "AUX"]}},
        {"OP": "+", "POS": {"NOT_IN": ["PUNCT"]}},  
        {"LEMMA": "ser", "POS": {"IN": ["AUX", "VERB"]}},
        {"LOWER": "lo"},
        {"LOWER": "mío"},
    ]
])


# --- Ironía ---
# Prefiero no mejorar mi vida
matcher.add("IRONIA_PREFIERO_NO", [
    [{"LEMMA": "preferir", "POS": "VERB"}, {"LOWER": "no"}, {"POS": "VERB"}],
])

# ¿Quién necesita aprender cosas nuevas?
matcher.add("IRONIA_QUIEN_NECESITA", [
    [{"LOWER": "quién"}, {"LEMMA": "necesitar", "POS": "VERB"}],
])

# Por qué habría de intentarlo
matcher.add("IRONIA_PORQUE_HABRIA_DE", [
    [{"LOWER": "por"}, {"LOWER": "qué"}, {"LEMMA": "haber", "POS": "AUX"}, {"LOWER": "de"}, {"POS": "VERB"}],
])

# --- Metáforas ---
# Ignorar las cosas importantes es mi hobby
matcher.add("META_VERBOS_ES_MI", [
    [
        {"LEMMA": {"IN": ["ignorar", "vivir", "ser", "estar", "perder", "arruinar", "hacer", "rechazar", "fracasar", "seguir"]}},
        {"OP": "*"},       # cualquier cosa entre verbo y "es mi"
        {"LOWER": "es"},
        {"LOWER": "mi"},
        {"OP": "+"}        # al menos un token después de "mi"
    ]
])


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
    matches = matcher(doc)  # matcher global con todos los patrones
    results = []

    for match_id, start, end in matches:
        span = doc[start:end]
        if span.text.lower() in SHAMING_EXCEPTIONS:
            continue  # ignorar excepciones definidas

        results.append({
            "text": span.sent.text,
            "path": path,
            "pattern": NLP.vocab.strings[match_id],  # nombre del patrón
        })

    return results


def is_an_exception(text):
    """
    Check if the text is in the list of exceptions.
    Args:
        text (str): The text to check.
    Returns:
        bool: True if the text is an exception, False otherwise.
    """
    return text.lower() in SHAMING_EXCEPTIONS

def contains_negative_terms(span):
    """
    Detecta términos negativos dentro de un span:
    - Tokens individuales usando lemma
    - Frases compuestas usando substring en texto normalizado
    """
    span_text = " ".join(span.text.lower().split())

    # Revisar tokens individuales
    for token in span:
        if token.lemma_.lower() in NEGATIVE_TERMS["verbos"] + NEGATIVE_TERMS["adjetivos"] + NEGATIVE_TERMS["sustantivos"]:
            return True

    # Revisar frases compuestas
    for phrase in NEGATIVE_TERMS["frases_compuestas"]:
        # reemplazamos múltiples espacios por uno solo
        phrase_norm = " ".join(phrase.lower().split())
        if phrase_norm in span_text:
            return True

    return False


def check_shaming_in_text(text):
    doc = NLP(text)
    matches = matcher(doc)
    if not matches:
        return False

    for match_id, start, end in matches:
        span = doc[start:end].sent
        if is_an_exception(span.text):
            continue

        rule_name = NLP.vocab.strings[match_id]

        # Para patrones de tipo FP_ES_LO_MIO, revisamos términos negativos
        if rule_name == "FP_ES_LO_MIO":
            if contains_negative_terms(span):
                return rule_name
        else:
            # Para otros patrones (IRONIA, META, FP_VERB), cualquier match ya es shaming
            return rule_name

    return False




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

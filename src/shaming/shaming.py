from config import NLP
from .matcher import create_matcher
from .patterns import exceptions, get_negative_adjectives, get_negative_nouns, get_negative_verbs, get_negative_phrases
import joblib
clf = joblib.load("shaming_svm.pkl")  # cargamos el modelo entrenado

matcher = create_matcher()


def is_an_exception(text):
    """
    Check if the text is in the list of exceptions.
    Args:
        text (str): The text to check.
    Returns:
        bool: True if the text is an exception, False otherwise.
    """
    return text.lower() in exceptions()

def contains_negative_terms(span):
    """
    Detecta términos negativos dentro de un span:
    - Tokens individuales usando lemma
    - Frases compuestas usando substring en texto normalizado
    """
    span_text = " ".join(span.text.lower().split())

    # Revisar tokens individuales
    for token in span:
        if token.lemma_.lower() in get_negative_verbs() + get_negative_adjectives() + get_negative_nouns():
            return True

    # Revisar frases compuestas
    for phrase in get_negative_phrases():
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

        # --- IA: verificar con el clasificador ---
        vec = span.vector.reshape(1, -1)
        prediction = clf.predict(vec)[0]
        confidence = clf.predict_proba(vec)[0][1]

        if prediction == 1:
            return {"pattern": rule_name, "ml_pred": True, "confidence": confidence}
        else:
            return {"pattern": rule_name, "ml_pred": False, "confidence": confidence}

    return False



def check_text_shaming_nopath(data):
    response = dict()
    response["Version"] = "0.3"
    response["ShamingInstances"] = []
    response["Path"] = data["Path"]

    # --- Título ---
    result = check_shaming_in_text(data["Title"])
    if result and result["ml_pred"]:
        response["Title"] = {"Text": data["Title"], "HasShaming": True, "ID": "Title", "Confidence": result["confidence"]}
    else:
        response["Title"] = {"Text": data["Title"], "HasShaming": False, "ID": "Title"}

    # --- Textos ---
    for text in data["Texts"]:
        result = check_shaming_in_text(text["Text"])
        if result and result["ml_pred"]:
            response["ShamingInstances"].append(
                {
                    "Text": text["Text"],
                    "HasShaming": True,
                    "ID": text["ID"],
                    "Confidence": result["confidence"]
                }
            )
        else:
            response["ShamingInstances"].append(
                {
                    "Text": text["Text"],
                    "HasShaming": False,
                    "ID": text["ID"]
                }
            )

    # --- Botones ---
    for button in data["Buttons"]:
        result = check_shaming_in_text(button["Label"])
        if result and result["ml_pred"]:
            response["ShamingInstances"].append(
                {
                    "Text": button["Label"],
                    "HasShaming": True,
                    "ID": button["ID"],
                    "Confidence": result["confidence"]
                }
            )
        else:
            response["ShamingInstances"].append(
                {
                    "Text": button["Label"],
                    "HasShaming": False,
                    "ID": button["ID"]
                }
            )

    return response




# Función del modelo viejo
def check_text_shaming(text, path):
    """
    Analiza un texto para identificar patrones de "shaming" 
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
        if span.text.lower() in exceptions():
            continue  # ignorar excepciones definidas

        results.append({
            "text": span.sent.text,
            "path": path,
            "pattern": NLP.vocab.strings[match_id],  # nombre del patrón
        })

    return results
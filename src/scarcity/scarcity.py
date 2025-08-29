from config import NLP
from spacy.matcher import Matcher

scarcity_matcher = Matcher(NLP.vocab)
scarcity_patterns = [
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
scarcity_matcher.add("fake_scarcity", scarcity_patterns)

def check_text_scarcity(text, path):
    """
    Analiza un texto para detectar patrones de escasez y devuelve las oraciones que coinciden.
    """
    doc = NLP(text)
    matches = scarcity_matcher(doc, as_spans=True)
    sentences = []
    for match in matches:
        sentences.append({
            "text": match.sent.text,
            "path": path,
            "pattern": "SCARCITY",
        })
    return sentences

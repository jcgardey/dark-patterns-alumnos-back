import json
import spacy
from spacy.matcher import Matcher  

from flask import Flask
from flask import request
from flask_cors import CORS

from datetime import datetime



app = Flask(__name__)
CORS(app)

nlp = spacy.load("es_core_news_sm")

# lista de palabras claves para detectar urgency
PATTERNS_URGENCY = ["limita","últi","sol", "apur","pierd","perd","ahora","ya","hoy","grat"]

# lista de palabras que no deberían considerarse en el matching de confirm shaming
SHAMING_EXCEPTIONS = ["inicio"]

# Fake Scarcity matcher
fake_scarcity_matcher = Matcher(nlp.vocab)
fake_scarcity_patterns = [
        [
            {"LOWER": {"FUZZY": {"IN": ["ultima", "ultimo"]}}},
            {"TEXT": {"REGEX": "^\d*"}, "OP": "?"},
            {"LOWER": {"FUZZY": {"IN": ["unidade", "disponible"]}}}
        ],
        [
            {"LOWER": {"FUZZY1": "solo"}},
            {"LOWER": {"FUZZY1": "queda"}},
            {"TEXT": {"REGEX": "^\d+"}},
        ]
]
fake_scarcity_matcher.add("fake_scarcity", fake_scarcity_patterns)


# First person verb matcher
first_person_matcher = Matcher(nlp.vocab)
first_person_verb_pattern = [
        # Verbos en primer persona
        [{"POS": "VERB", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}}],
        # Oraciones del tipo "Soy una mala persona". Detecta "Soy"
        [{"DEP": "cop", "POS": "AUX", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}}],
        # Oraciones del tipo "Me gusta...". Detecta "Me" + VERBO
        [
            {"POS": "PRON", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}},
            {"POS": "VERB"}
        ],
        # Oraciones del tipo "Me voy a hacer...". Detecta "Voy" + "a" + VERBO
        [
            {"DEP": "aux", "POS": "AUX", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}},
            {"DEP": "mark", "POS": "ADP"}, {"POS": "VERB"}
        ],
]
first_person_matcher.add("first_person", first_person_verb_pattern)

# "No, thanks" matcher
negation_matcher = Matcher(nlp.vocab)
negation_pattern = [{"LOWER": "no"}]
negation_matcher.add("negation", [negation_pattern])

# Hardcoded examples
file = open("examples_es.json", "r")
examples_str = file.read()
file.close()
examples_list = json.loads(examples_str)

@app.post("/shaming")
def detect_shaming():
    sentences = []
    tokens = request.get_json().get('tokens')
    #tokens.extend(examples_list)
    for token in tokens:
        sentences.extend(check_text_shaming(token["text"], token["path"]))
    return sentences

@app.post("/urgency")
def detect_urgency():
    sentences = []
    tokens = request.get_json().get('tokens')
    for token in tokens:
        sentences.extend(check_text_urgency(token["text"], token["path"]))
    return sentences


def check_text_shaming(text, path):
    doc = nlp(text)
    # Match first person verbs
    first_person_matches = first_person_matcher(doc, as_spans=True)

    sentences = []
    if first_person_matches:
        # Check for exceptions
        if first_person_matches[0].text.lower() in SHAMING_EXCEPTIONS:
            return []
        print(first_person_matches[0].sent.text, first_person_matches[0].text)
        sentences.append({
            "text": first_person_matches[0].sent.text,
            "path": path,
            "pattern": "SHAMING"
            })
    return sentences


def check_text_urgency(text, path):
    doc = nlp(text)
    fake_scarcity_matches = fake_scarcity_matcher(doc, as_spans=True)

    sentences = []
    if fake_scarcity_matches:
        print(fake_scarcity_matches[0].sent.text, fake_scarcity_matches[0].text)
        sentences.append({
            "text": fake_scarcity_matches[0].sent.text,
            "path": path,
            "pattern": "URGENCY"
            })
    return sentences
    """
    if detect_urgency(doc, PATTERNS_URGENCY):
        print(text)
        sentences.append({
            "text": text,
            "path": path,
            "pattern": "URGENCY"
            })
    """



def detect_urgency(doc,p):
    for token in doc:
        if(token.pos_ != "PUNCT"):
            for patron in p:
                if patron in token.text.lower():
                    return True
    return False

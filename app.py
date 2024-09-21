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
#nlp = spacy.load("es_dep_news_trf")

# lista de palabras claves para detectar urgency
PATTERNS_URGENCY = ["limita","últi","sol", "apur","pierd","perd","ahora","ya","hoy","grat"]

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

@app.post("/")
def hello_world():
    sentences = []
    tokens = request.get_json().get('tokens')
    #tokens.extend(examples_list)
    for token in tokens:
        sentences.extend(check_text(token))
    return sentences


def check_text(text):
    doc = nlp(text)
    for token in doc:
        print(token.text, token.dep_, token.pos_, token.morph)
    # Match first person verbs
    first_person_matches = first_person_matcher(doc, as_spans=True)

    sentences = []
    if first_person_matches:
        print(first_person_matches[0].sent.text, first_person_matches[0].text)
        sentences.append({
            "text": first_person_matches[0].sent.text,
            "pattern": "SHAMING"
            })
    if detect_urgency(doc, PATTERNS_URGENCY):
        print(text)
        sentences.append({
            "text": text,
            "pattern": "URGENCY"
            })
    return sentences



def detect_urgency(doc,p):
    for token in doc:
        if(token.pos_ != "PUNCT"):
            for patron in p:
                if patron in token.text.lower():
                    return True
    return False

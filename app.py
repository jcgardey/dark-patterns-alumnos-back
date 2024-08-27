import json
import spacy
from spacy.matcher import Matcher  

from flask import Flask
from flask import request
from flask_cors import CORS

from datetime import datetime



app = Flask(__name__)
CORS(app)

#nlp = spacy.load("es_core_news_sm")
nlp = spacy.load("es_dep_news_trf")

# First person verb matcher
first_person_matcher = Matcher(nlp.vocab)
first_person_verb_pattern = [
        [{"POS": "VERB", "MORPH": {"IS_SUPERSET": ["Person=1"]}}],
        [{"DEP": "iobj", "POS": "PRON", "MORPH": {"IS_SUPERSET": ["Person=1"]}}, {"POS": "VERB"}],
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
    tokens.extend(examples_list)
    for token in tokens:
        sentences.extend(check_text(token))
    return sentences


def check_text(text):
    doc = nlp(text)
    # Match first person verbs
    first_person_matches = first_person_matcher(doc, as_spans=True)

    sentences = []
    for span in first_person_matches:
        print(span.sent.text, span.text, span.label_)
        negation_matches = negation_matcher(span.sent, as_spans=True)
        # Si hay muchos "no" en la oración, me quedo con el primero
        if negation_matches:
            sentences.append(negation_matches[0].sent.text)
    return sentences

from spacy.matcher import Matcher
from config import NLP
from .patterns import get_patterns

def create_matcher():
    matcher = Matcher(NLP.vocab)
    patterns = get_patterns()
    for name, pattern in patterns.items():
        matcher.add(name, pattern)
    return matcher

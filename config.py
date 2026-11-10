import os
import spacy

# Deshabilitar 'ner' ya que los matchers y SVM se basan en sintaxis/tokens/vectores
# Esto reduce el tiempo de inferencia a más de la mitad y ahorra memoria
DISABLED_PIPES = ["ner"]
MODEL_NAME = os.getenv("SPACY_MODEL", "es_core_news_lg")

try:
    NLP = spacy.load(MODEL_NAME, disable=DISABLED_PIPES)
except OSError:
    print(f"Descargando modelo '{MODEL_NAME}'. Esto puede tardar un poco...")
    spacy.cli.download(MODEL_NAME)
    NLP = spacy.load(MODEL_NAME, disable=DISABLED_PIPES)

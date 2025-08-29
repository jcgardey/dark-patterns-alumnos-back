import spacy

try:
    NLP = spacy.load("es_core_news_lg") # O "es_core_news_lg" para más robustez
except OSError:
    print("Descargando modelo 'es_core_news_lg'. Esto puede tardar un poco...")
    spacy.cli.download("es_core_news_lg")
    NLP = spacy.load("es_core_news_lg")
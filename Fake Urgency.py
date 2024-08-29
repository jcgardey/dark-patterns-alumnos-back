import  spacy
from spacytextblob.spacytextblob import SpacyTextBlob



def detect_urgency(text,p):
    doc = nlp(text)
    Fake_U=False
    for token in doc:
        if(token.pos_ != "PUNCT"):
            for patron in p:
                if patron in token.text:
                    Fake_U=True
    return Fake_U



nlp = spacy.load("es_core_news_lg")
nlp.add_pipe("spacytextblob")
patronesRaiz = ["limita","ulti","sol", "apur","pierd","perd","ahora","ya","hoy","grat"]
texto="Ultimos (1 disponible)"
texto=texto.lower()


if(detect_urgency(texto,patronesRaiz)):
    print("FAKE URGENCY DETECTADO")
else:
    print("NO ES FAKE URGENCY")


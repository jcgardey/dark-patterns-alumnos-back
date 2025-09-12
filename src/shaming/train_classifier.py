import pandas as pd
import spacy
from sklearn.svm import SVC
import joblib
import os

# Ruta al dataset
BASE_DIR = os.path.dirname(__file__)  # carpeta donde está train_classifier.py
DATA_PATH = os.path.join(BASE_DIR, "shaming_dataset.csv")

# Cargar spaCy en español
nlp = spacy.load("es_core_news_md")

# Leer dataset CSV
df = pd.read_csv(DATA_PATH)  # columnas: "text", "label"
print(f"Dataset cargado con {len(df)} ejemplos.")

# Vectorizar cada frase con spaCy
X = [nlp(text).vector for text in df["text"]]
y = df["label"].values

# Entrenar clasificador SVM
clf = SVC(kernel="linear", probability=True)
clf.fit(X, y)

# Guardar el modelo en disco
joblib.dump(clf, "shaming_svm.pkl")
print("Modelo entrenado y guardado en shaming_svm.pkl")

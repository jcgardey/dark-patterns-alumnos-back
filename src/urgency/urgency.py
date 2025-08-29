"""
Este módulo detecta patrones de urgencia en textos usando spaCy.

Incluye dos tipos de matchers:
- PhraseMatcher: detecta coincidencias exactas de frases típicas de urgencia
  (ej: "ventas flash", "compre ya", "última oportunidad", "limited time offer").
- Matcher: detecta patrones estructurales flexibles, como verbos imperativos
  combinados con palabras de urgencia, o frases como
  "no se quede fuera", "la promoción termina pronto", "quedan pocas horas".

Esto permite cubrir tanto frases hardcodeadas como variantes y estructuras
comunes de urgencia comercial (dark patterns).
"""

from config import NLP
from spacy.matcher import PhraseMatcher, Matcher
from .types import UrgencyRequestSchema, UrgencyResponseSchema

# ------------------------------
# PhraseMatcher para coincidencias exactas
# ------------------------------
urgency_phrase_matcher = PhraseMatcher(NLP.vocab, attr="LOWER")

frases_urgencia = [
    # Español
    "ventas flash",
    "venta flash",
    "ventas relampago",
    "compre ya",
    "no se quede fuera", # Aunque tiene imperativo, la combinación es muy específica
    "última oportunidad", # Puede ser estructural, pero como frase hecha es muy común
    "oferta especial",
    "oferta única",
    "solo hoy",
    "solo por hoy",
    "descuento por tiempo limitado", # Podría ser estructural, pero es una frase muy concreta
    "promoción limitada", # Similar al anterior
    # Inglés
    "flash sale",
    "flash deals",
    "limited time offer", # Aunque tiene "limited time", es una frase hecha
    "hurry up",
    "last chance", # Similar a "última oportunidad"
    "offer ends soon", # "ends soon" se puede coger con la otra regla
    "limited offer", # Similar a "oferta limitada"
    "time is running out", # Es una frase idiomática
]

patterns = [NLP.make_doc(frase) for frase in frases_urgencia]
urgency_phrase_matcher.add("URGENCIA_PHRASE", patterns)


# ------------------------------
# Matcher estructural para patrones flexibles
# ------------------------------
urgency_matcher = Matcher(NLP.vocab)

# Imperativo + urgencia
urgency_matcher.add(
    "URGENT_IMPERATIVE",
    [
        [
            {
                "LEMMA": {
                    "IN": [
                        "comprar",
                        "aprovechar",
                        "entrar",
                        "participar",
                        "apresurarse",
                        "adquirir",
                    ]
                },
                "POS": "VERB",
                "MORPH": {"IS_SUPERSET": ["Mood=Imp"]},
            },
            {"LOWER": {"IN": ["ya", "ahora", "mismo"]}, "OP": "?"},
        ],
        [
            {"LOWER": {"IN": ["no"]}},
            {"LEMMA": {"IN": ["quedar", "perder"]}},
            {"LOWER": {"IN": ["fuera", "atrás", "oportunidad"]}},
        ],
        [
            {
                "LEMMA": {
                    "IN": [
                        "comprar",
                        "aprovechar",
                        "entrar",
                        "participar",
                        "apresurarse",
                        "adquirir",
                    ]
                },
                "POS": "VERB",
                "MORPH": {"IS_SUPERSET": ["Mood=Imp"]},
            },
            {"LOWER": {"IN": ["ya", "ahora", "mismo"]}, "OP": "?"},
        ],
    ],
)

# Oferta/Promoción que termina
urgency_matcher.add(
    "URGENT_OFFER_ENDING",
    [
        [
            {"LOWER": {"IN": ["la", "esta"]}, "OP": "?"},
            {"LOWER": {"IN": ["oferta", "promoción", "venta", "descuento"]}},
            {"LEMMA": {"IN": ["terminar", "finalizar", "acabar"]}},
            {"LOWER": {"IN": ["pronto", "ya", "hoy"]}, "OP": "?"},
        ]
    ],
)

# Última oportunidad
urgency_matcher.add(
    "URGENT_LAST_CHANCE",
    [
        [
            {"LOWER": {"IN": ["última", "último", "últimas", "últimos"]}},
            {
                "LOWER": {
                    "IN": ["oportunidad", "chance", "posibilidad", "días", "horas"]
                }
            },
        ],
        [{"LOWER": {"IN": ["last"]}}, {"LOWER": {"IN": ["chance", "opportunity"]}}],
    ],
)

# Tiempo limitado
urgency_matcher.add(
    "URGENT_TIME_LIMIT",
    [
        [
            {"LOWER": {"IN": ["tiempo", "oferta"]}},
            {"LOWER": {"IN": ["limitado", "limitada"]}},
        ],
        [{"LOWER": {"IN": ["limited"]}}, {"LOWER": {"IN": ["time", "offer"]}}],
    ],
)

# Quedan X horas/días (para usar cuando frontend detecta reloj y manda contexto)
urgency_matcher.add(
    "URGENT_FEW_LEFT",
    [
        [
            {"LOWER": {"IN": ["oferta", "promoción", "descuento", "venta"]}},  # palabra comercial obligatoria
            {"LEMMA": {"IN": ["quedar", "faltar"]}},
            {"LOWER": {"IN": ["pocas", "solo", "únicas"]}, "OP": "?"},
            {"LOWER": {"IN": ["horas", "días", "minutos", "semanas"]}},
        ],
        [
            {"LOWER": {"IN": ["only"]}},
            {"LIKE_NUM": True},
            {"LOWER": {"IN": ["hours", "days", "minutes", "left"]}},
        ],
    ],
)


# Ends soon
urgency_matcher.add(
    "URGENT_ENDS_SOON",
    [
        [
            {"LOWER": {"IN": ["ends", "ending"]}},
            {"LOWER": {"IN": ["soon", "today", "now"]}, "OP": "?"},
        ]
    ],
)

# Hurry up / apúrate
urgency_matcher.add(
    "URGENT_HURRY",
    [
        [
            {"LEMMA": {"IN": ["apresurarse", "apurar", "aprovechar"]}},
            {"LOWER": {"IN": ["ya", "ahora", "mismo"]}, "OP": "?"},
        ],
        [
            {"LOWER": {"IN": ["hurry", "rush"]}},
            {"LOWER": {"IN": ["up", "now"]}, "OP": "?"},
        ],
    ],
)


# ------------------------------
# Funciones principales
# ------------------------------
def check_text_urgency(text, path):
    """
    Analiza un texto para detectar patrones de urgencia (no escasez)
    y devuelve lista de dicts con text, path, pattern.
    """
    doc = NLP(text)
    results = []
    # Coincidencias exactas
    for match_id, start, end in urgency_phrase_matcher(doc):
        span = doc[start:end]
        results.append(
            {
                "text": span.sent.text,
                "path": path,
                "pattern": "PHRASE:" + NLP.vocab.strings[match_id],
            }
        )
    # Coincidencias estructurales
    for match_id, start, end in urgency_matcher(doc):
        span = doc[start:end]
        results.append(
            {
                "text": span.sent.text,
                "path": path,
                "pattern": "MATCH:" + NLP.vocab.strings[match_id],
            }
        )
    return results


def check_text_urgency_schema(data):
    """
    Recibe un dict validado por UrgencyRequestSchema
    y devuelve la respuesta serializada por UrgencyResponseSchema.
    """
    urgency_instances = []
    for token in data["tokens"]:
        urgency_instances.extend(check_text_urgency(token["text"], token["path"]))
    response_schema = UrgencyResponseSchema()
    response = {"Version": data["Version"], "UrgencyInstances": urgency_instances}
    return response_schema.dump(response)

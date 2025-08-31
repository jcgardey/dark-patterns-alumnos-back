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

import unicodedata
from config import NLP
from spacy.matcher import Matcher
from .types import UrgencyResponseSchema


frases_urgencia = [
    "ventas flash",
    "venta flash",
    "oferta flash",
    "ventas relampago",
    "compre ya",
    "compra ya",
    "promoción relampago",
    "promoción relámpago",
    "promocion relampago",
    "promoción flash",
    "no se quede fuera",
    "última oportunidad",
    "oferta especial",
    "oferta única",
    "solo hoy",
    "solo por hoy",
    "descuento por tiempo limitado",
    "promoción limitada",
    "flash sale",
    "flash deals",
    "limited time offer",
    "hurry up",
    "last chance",
    "offer ends soon",
    "limited offer",
    "time is running out",
    "apresúrate",
    "tiempo restante",
    "ofertas por dia",
    "ofertas por día",
    "cupon",
    "cupón",
    "mega oferta",
    "última oportunidad",
    "super oferta"
]


urgency_matcher = Matcher(NLP.vocab)

for texto in frases_urgencia:
    doc_frase = NLP(texto)
    pattern = [{"LOWER": token.lower_} for token in doc_frase]
    urgency_matcher.add("URGENCIA_PHRASE", [pattern])

urgency_matcher.add(
    "URGENT_IMPERATIVE_DIRECT",
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
                        "obtener",
                        "reservar",
                        "haz",
                    ]
                },
                "POS": "VERB",
                "MORPH": {"IS_SUPERSET": ["Mood=Imp"]},
            },
            {"LOWER": {"IN": ["ya", "ahora", "mismo", "hoy"]}, "OP": "?"},
        ],
    ],
)

urgency_matcher.add(
    "URGENT_IMPERATIVE_SIMPLE",
    [
        [
            {
                "POS": "VERB",
                "MORPH": {"IS_SUPERSET": ["Mood=Imp"]},
                "LEMMA": {"IN": ["comprar", "hacer", "aprovechar", "venir", "ir"]},
            },
        ],
    ],
)

urgency_matcher.add(
    "URGENT_DONT_MISS_OUT",
    [
        [
            {"LOWER": {"IN": ["no"]}},
            {
                "POS": {"IN": ["PRON", "ADV", "DET", "ADP"]},
                "OP": "*",
            },
            {"LEMMA": {"IN": ["quedar", "perder", "dejar"]}},
            {
                "POS": {"IN": ["PRON", "ADV", "ADP", "DET"]},
                "OP": "*",
            },
            {"LOWER": {"IN": ["fuera", "atrás", "oportunidad", "pasar", "esto"]}},
        ],
    ],
)

urgency_matcher.add(
    "URGENT_OFFER_ENDING_VERB",
    [
        [
            {"LOWER": {"IN": ["la", "esta", "el", "este"]}, "OP": "?"},
            {"LOWER": {"IN": ["oferta", "promoción", "venta", "descuento"]}},
            {
                "POS": {"IN": ["ADJ"]},
                "OP": "*",
            },  # Solo adjetivos que describan la oferta.
            {
                "LEMMA": {
                    "IN": ["terminar", "finalizar", "acabar", "expirar", "validar"]
                }
            },
            {
                "LOWER": {
                    "IN": [
                        "pronto",
                        "ya",
                        "hoy",
                        "mañana",
                        "esta",
                        "este",
                        "la",
                        "el",
                        "en",
                        "antes",
                        "hasta",
                    ]
                },
                "OP": "*",
            },
            {
                "LOWER": {
                    "IN": [
                        "semana",
                        "mes",
                        "día",
                        "noche",
                        "oportunidad",
                        "minutos",
                        "horas",
                        "dias",
                        "medianoche",
                        "mediodia",
                    ]
                },
                "OP": "?",
            },
            {"LIKE_NUM": True, "OP": "?"},
            {"LOWER": {"IN": ["minutos", "horas", "días", "semanas"]}, "OP": "?"},
        ],
        [
            {
                "LEMMA": {
                    "IN": ["finalizar", "terminar", "acabar", "expirar", "vencer"]
                },
                "IS_SENT_START": True,
            },
            {"LOWER": "en", "OP": "?"},
            {"IS_ALPHA": False, "OP": "+"},
            {
                "LOWER": {"IN": ["minutos", "horas", "días", "semanas", "h", "m", "s"]},
                "OP": "*",
            },
        ],
        [
            {"LOWER": {"IN": ["la", "esta", "el", "este"]}, "OP": "?"},
            {"LOWER": {"IN": ["oferta", "promoción", "venta", "descuento"]}},
            {"LEMMA": "válido"},
            {"LOWER": "hasta"},
            {"LOWER": {"IN": ["medianoche", "mediodia", "hoy", "mañana", "noche"]}},
        ],
    ],
)

urgency_matcher.add(
    "URGENT_OFFER_ENDING_BEFORE",
    [
        [
            {"LOWER": {"IN": ["antes"]}},
            {"LOWER": {"IN": ["de"]}},
            {"LOWER": {"IN": ["que"]}},
            {"LOWER": {"IN": ["se"]}, "OP": "?"},
            {"LEMMA": {"IN": ["acabar", "terminar", "agotar", "finalizar", "expirar"]}},
        ],
    ],
)

urgency_matcher.add(
    "URGENT_LAST_CHANCE",
    [
        [
            {"LOWER": {"IN": ["última", "último", "últimas", "últimos"]}},
            {
                "LOWER": {
                    "IN": [
                        "oportunidad",
                        "chance",
                        "posibilidad",
                        "días",
                        "horas",
                        "cupos",
                        "plazas",
                    ]
                }
            },
        ],
        [{"LOWER": {"IN": ["last"]}}, {"LOWER": {"IN": ["chance", "opportunity"]}}],
    ],
)

urgency_matcher.add(
    "URGENT_TIME_LIMIT",
    [
        [
            {"LOWER": {"IN": ["tiempo", "oferta", "promoción", "descuento"]}},
            {"LOWER": {"IN": ["limitado", "limitada"]}},
        ],
        [{"LOWER": {"IN": ["limited"]}}, {"LOWER": {"IN": ["time", "offer"]}}],
    ],
)

urgency_matcher.add(
    "URGENT_DONT_MISS_OUT",
    [
        [
            {"LOWER": "no"},
            {"POS": {"IN": ["PRON", "ADV", "DET", "ADP"]}, "OP": "*"},
            {"LEMMA": "quedes"},
            {"LOWER": "fuera"},
            {"POS": {"IN": ["ADP", "DET"]}, "OP": "*"},
            {
                "LOWER": {
                    "IN": [
                        "oportunidad",
                        "promoción",
                        "esto",
                        "ganga",
                        "oferta",
                        "evento",
                    ]
                }
            },
        ],
        [
            {"LOWER": "no"},
            {"POS": {"IN": ["PRON", "ADV", "DET", "ADP"]}, "OP": "*"},
            {"LEMMA": {"IN": ["perder", "dejar"]}},
            {"POS": {"IN": ["PRON", "ADV", "ADP", "DET"]}, "OP": "*"},
            {
                "LOWER": {
                    "IN": [
                        "oportunidad",
                        "pasar",
                        "esto",
                        "promoción",
                        "ganga",
                        "oferta",
                        "evento",
                    ]
                }
            },
        ],
        [
            {
                "LOWER": {
                    "IN": [
                        "envío",
                        "oferta",
                        "promoción",
                        "descuento",
                        "venta",
                        "plazo",
                    ]
                }
            },
            {"POS": {"IN": ["ADJ", "ADV", "DET", "NOUN", "PROPN"]}, "OP": "*"},
            {"LEMMA": {"IN": ["terminar", "acabar", "expirar", "finalizar"]}},
            {
                "LOWER": {
                    "IN": ["pronto", "hoy", "ya", "ahora", "inmediatamente", "mañana"]
                }
            },
        ],
        [
            {"LOWER": {"IN": ["último", "final", "solo"]}},
            {"POS": {"IN": ["ADJ", "DET", "ADV"]}, "OP": "*"},
            {"LOWER": {"IN": ["oportunidad", "día", "horas", "momentos", "chance"]}},
        ],
        [
            {"LEMMA": "quedar"},
            {"POS": {"IN": ["DET", "NUM"]}, "OP": "+"},
            {
                "LOWER": {
                    "IN": ["días", "horas", "minutos", "cupos", "plazas", "unidades"]
                }
            },
        ],
    ],
)

urgency_matcher.add(
    "URGENT_ENDS_SOON",
    [
        [
            {"LOWER": {"IN": ["ends", "ending"]}},
            {"LOWER": {"IN": ["soon", "today", "now"]}, "OP": "?"},
        ]
    ],
)

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


urgency_matcher.add(
    "PERCENTAGE",
    [
        [  # 👈 lista extra que envuelve el patrón
            {"TEXT": {"REGEX": r"^\d{1,2}:\d{2}:\d{2}$"}},  # hora
            {"TEXT": {"REGEX": r"^-?\d+%$"}},  # porcentaje
        ],
        [
            {"TEXT": {"REGEX": r"^\d+(\.\d+)?%$"}},  # número con opcional decimal + %
            {"LOWER": "de"},
            {"LOWER": "descuento"},
        ],
    ],
)


def check_text_urgency(text, path):
    """
    Analiza un texto para detectar patrones de urgencia (no escasez)
    y devuelve True si detecta al menos un patrón.
    """
    doc = NLP(text)
    for _ in urgency_matcher(doc):
        return True
    return False


def check_text_urgency_schema(data):
    """
    Recibe un dict validado por UrgencyRequestSchema
    y devuelve la respuesta serializada por UrgencyResponseSchema.
    """
    urgency_instances = []
    for current_analized_text in data["texts"]:
        text = current_analized_text["text"]
        id_ = current_analized_text.get("id")
        path = current_analized_text.get("path")
        has_urgency = check_text_urgency(text, path)
        instance = {"text": text, "has_urgency": has_urgency}
        if id_ is not None:
            instance["id"] = id_
        if path is not None:
            instance["path"] = path
        urgency_instances.append(instance)
    response_schema = UrgencyResponseSchema()
    response = {"version": data["version"], "urgency_instances": urgency_instances}
    return response_schema.dump(response)

from config import NLP
from spacy.matcher import Matcher

matcher = Matcher(NLP.vocab)

SHAMING_EXCEPTIONS = ["inicio"]
NEGATIVE_TERMS = {
    "verbos": ["ignorar", "mentir", "criticar", "procrastinar", "romper reglas", "cometer errores",
               "desobedecer", "manipular", "vengar", "envidiar",
    ],
    "adjetivos": ["desordenado", "egoísta", "sarcástico", "impuntual", "hiriente", "arrogante",
                  "grosero", "malhumorado", "perezoso", "despreocupado", "irritable", "intolerante",
                  "rudo", "desconsiderado", "cínico", "descuidado", "apático", "negligente",
                  "insensible", "deshonesto", "desagradable", "celoso", "resentido", "irresponsable",
                  "negativo", "ignorante"
    ],
    "sustantivos": ["bromas pesadas", "egoísmo", "irresponsabilidad", "deslealtad",
                    "bullying", "injusticia", "impaciencia",
    ],
    "frases_compuestas": ["promesas que no cumplo", "hacer caso omiso", "hacer lo mínimo posible",
        "seguir cometiendo los mismos errores", "seguir evitando responsabilidades", "seguir ignorando consejos",
        "seguir ignorando soluciones fáciles", "a último momento"
    ]
}
ALL_NEGATIVE_TERMS = (
    NEGATIVE_TERMS["verbos"] +
    NEGATIVE_TERMS["adjetivos"] +
    NEGATIVE_TERMS["sustantivos"] +
    NEGATIVE_TERMS["frases_compuestas"]
)
def get_negative_terms():
    return ALL_NEGATIVE_TERMS

def get_negative_verbs():
    return NEGATIVE_TERMS["verbos"]

def get_negative_adjectives():
    return NEGATIVE_TERMS["adjetivos"]

def get_negative_nouns():
    return NEGATIVE_TERMS["sustantivos"]

def get_negative_phrases():
    return NEGATIVE_TERMS["frases_compuestas"]

def exceptions():
    return SHAMING_EXCEPTIONS

def get_patterns():
    return {
        # Primera persona
        "FP_VERB": [[{"POS": "VERB", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}}]],
        "FP_COPULA": [[{"DEP": "cop", "POS": "AUX", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}}]],
        "FP_ME_VERB": [[{"POS": "PRON", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}}, {"POS": "VERB"}]],

        # Perífrasis
        "FP_PERIFRASIS_VOY_A": [[
            {"DEP": "aux", "POS": "AUX", "MORPH": {"IS_SUPERSET": ["Person=1", "Number=Sing"]}},
            {"DEP": "mark", "POS": "ADP"},
            {"POS": "VERB"},
        ]],

        # Ser desordenado es lo mío
        "FP_ES_LO_MIO": [[
            {"LEMMA": {"IN": ["seguir", "ignorar", "ser", "hacer"]}, "POS": {"IN": ["VERB", "AUX"]}},
            {"OP": "+", "POS": {"NOT_IN": ["PUNCT"]}},
            {"LEMMA": "ser", "POS": {"IN": ["AUX", "VERB"]}},
            {"LOWER": "lo"},
            {"LOWER": "mío"},
        ]],

        # Ironía
        "IRONIA_PREFIERO_NO": [[{"LEMMA": "preferir", "POS": "VERB"}, {"LOWER": "no"}, {"POS": "VERB"}]],
        "IRONIA_QUIEN_NECESITA": [[{"LOWER": "quién"}, {"LEMMA": "necesitar", "POS": "VERB"}]],
        "IRONIA_PORQUE_HABRIA_DE": [[
            {"LOWER": "por"}, {"LOWER": "qué"}, {"LEMMA": "haber", "POS": "AUX"}, {"LOWER": "de"}, {"POS": "VERB"}
        ]],

        # Metáforas
        "META_VERBOS_ES_MI": [[
            {"LEMMA": {"IN": ["ignorar", "vivir", "ser", "estar", "perder", "arruinar", "hacer", "rechazar", "fracasar", "seguir"]}},
            {"OP": "*"},
            {"LOWER": "es"},
            {"LOWER": "mi"},
            {"OP": "+"}
        ]],
    }

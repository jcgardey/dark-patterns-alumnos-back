import marshmallow

class UrgencyTextSchema(marshmallow.Schema):
    """
    Esquema para validar y serializar datos de texto de urgencia.

    JSON esperado:
    {
        "text": "Texto a analizar",  # Obligatorio
        "id": "123",                 # Opcional
        "path": "/ruta/opcional"     # Opcional
    }

    Atributos:
        text (str): Obligatorio. El texto que se analizará.
        id (str, opcional): Identificador opcional del texto.
        path (str, opcional): Ruta opcional del texto.
    """
    text = marshmallow.fields.String(required=True, metadata={"description": "Texto a analizar."})
    id = marshmallow.fields.String(required=False, metadata={"description": "Identificador opcional del texto."})
    path = marshmallow.fields.String(required=False, metadata={"description": "Ruta opcional del texto."})

class UrgencyRequestSchema(marshmallow.Schema):
    """
    Esquema para validar datos de solicitud de urgencia.

    JSON esperado:
    {
        "version": "1.0",  
        "texts": [
            {
                "text": "Texto 1",
                "id": "id1",
                "path": "/ruta1"
            },
            {
                "text": "Texto 2"
            }
        ]
    }

    Atributos:
        version (str): Obligatorio. Versión del esquema.
        texts (List[UrgencyTextSchema]): Obligatorio. Lista de textos de urgencia.
    """
    version = marshmallow.fields.String(required=True, metadata={"description": "Versión del esquema."})
    texts = marshmallow.fields.List(marshmallow.fields.Nested(UrgencyTextSchema), required=True)

class UrgencyInstanceSchema(marshmallow.Schema):
    """
    Esquema para representar una instancia de urgencia.

    JSON esperado:
    {
        "text": "Texto de la instancia",  # Obligatorio
        "has_urgency": true,              # Obligatorio
        "id": "123",                        # Opcional
        "path": "/ruta/opcional"           # Opcional
    }

    Atributos:
        text (str): Obligatorio. Texto asociado a la instancia de urgencia.
        has_urgency (bool): Obligatorio. Indica si el texto tiene urgencia.
        id (str, opcional): Identificador opcional de la instancia.
    """
    text = marshmallow.fields.String(required=True)
    has_urgency = marshmallow.fields.Boolean(required=True)
    id = marshmallow.fields.String(required=False)
    path = marshmallow.fields.String(required=False)

class UrgencyResponseSchema(marshmallow.Schema):
    """
    Esquema para representar la respuesta de urgencia.

    JSON esperado:
    {
        "version": "1.0",  
        "urgency_instances": [
            {
                "text": "Texto 1",
                "has_urgency": true,
                "id": "id1",
                "path":"/opt"
            },
            {
                "text": "Texto 2",
                "has_urgency": false
            }
        ],
    }

    Atributos:
        version (str): Obligatorio. Versión de la respuesta.
        urgency_instances (List[UrgencyInstanceSchema]): Obligatorio. Lista de instancias de urgencia.
    """
    version = marshmallow.fields.String(required=True)
    urgency_instances = marshmallow.fields.List(marshmallow.fields.Nested(UrgencyInstanceSchema), required=True)

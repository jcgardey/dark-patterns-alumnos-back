import marshmallow

class TextSchema(marshmallow.Schema):
    """
    Esquema para validar y serializar datos de texto.

    JSON esperado:
    {
        "text": "Texto a analizar",   # Obligatorio
        "path": "/ruta/asociada",     # Obligatorio
        "id": "123"                   # Opcional
    }

    Atributos:
        text (str): Obligatorio. Texto a analizar.
        path (str): Obligatorio. Ruta asociada al texto.
        id (str, opcional): Identificador opcional del texto.
    """
    text = marshmallow.fields.String(required=True, metadata={"description": "Texto a analizar."})
    path = marshmallow.fields.String(required=False, metadata={"description": "Ruta asociada al texto."})
    id = marshmallow.fields.String(required=False, metadata={"description": "Identificador opcional del texto."})

class ScarcityRequestSchema(marshmallow.Schema):
    """
    Esquema para validar una solicitud de escasez de textos.

    JSON esperado:
    {
        "version": "1.0",  
        "texts": [
            {
                "text": "Texto 1",
                "path": "/ruta1",
                "id": "id1"
            },
            {
                "text": "Texto 2",
                "path": "/ruta2"
            }
        ]
    }

    Atributos:
        version (str): Obligatorio. Versión del esquema.
        texts (List[TextSchema]): Obligatorio. Lista de textos a analizar.
    """
    version = marshmallow.fields.String(required=True, metadata={"description": "Versión del esquema."})
    texts = marshmallow.fields.List(marshmallow.fields.Nested(TextSchema), required=True)

class ScarcityInstanceSchema(marshmallow.Schema):
    """
    Esquema para representar una instancia de escasez.

    JSON esperado:
    {
        "text": "Texto de la instancia",   # Obligatorio
        "path": "/ruta/asociada",          # Obligatorio
        "id": "123",                        # Opcional
        "has_scarcity": true                # Obligatorio
    }

    Atributos:
        text (str): Obligatorio. Texto de la instancia.
        path (str): Obligatorio. Ruta asociada al texto.
        id (str, opcional): Identificador opcional de la instancia.
        has_scarcity (bool): Obligatorio. Indica si hay escasez en el texto.
    """
    text = marshmallow.fields.String(required=True)
    path = marshmallow.fields.String(required=False)
    id = marshmallow.fields.String(required=False)
    has_scarcity = marshmallow.fields.Boolean(required=True)

class ScarcityResponseSchema(marshmallow.Schema):
    """
    Esquema para representar la respuesta de escasez.

    JSON esperado:
    {
        "version": "1.0",  
        "instances": [
            {
                "text": "Texto 1",
                "path": "/ruta1",
                "id": "id1",
                "has_scarcity": true
            },
            {
                "text": "Texto 2",
                "path": "/ruta2",
                "has_scarcity": false
            }
        ]
    }

    Atributos:
        version (str): Obligatorio. Versión de la respuesta.
        instances (List[ScarcityInstanceSchema]): Obligatorio. Lista de instancias de escasez.
    """
    version = marshmallow.fields.String(required=True)
    instances = marshmallow.fields.List(marshmallow.fields.Nested(ScarcityInstanceSchema), required=True)

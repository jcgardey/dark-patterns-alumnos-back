import marshmallow

class UrgencyTextSchema(marshmallow.Schema):
    text = marshmallow.fields.String(required=True, metadata={"description": "Texto a analizar."})
    id = marshmallow.fields.String(required=False, metadata={"description": "Identificador opcional del texto."})
    path = marshmallow.fields.String(required=False, metadata={"description": "Ruta opcional del texto."})

class UrgencyRequestSchema(marshmallow.Schema):
    version = marshmallow.fields.String(required=True, metadata={"description": "Versión del esquema."})
    texts = marshmallow.fields.List(marshmallow.fields.Nested(UrgencyTextSchema), required=True)

class UrgencyInstanceSchema(marshmallow.Schema):
    text = marshmallow.fields.String(required=True)
    has_urgency = marshmallow.fields.Boolean(required=True)
    id = marshmallow.fields.String(required=False)

class UrgencyResponseSchema(marshmallow.Schema):
    version = marshmallow.fields.String(required=True)
    urgency_instances = marshmallow.fields.List(marshmallow.fields.Nested(UrgencyInstanceSchema), required=True)
    path = marshmallow.fields.String(required=False, metadata={"description": "Ruta opcional de la respuesta."})

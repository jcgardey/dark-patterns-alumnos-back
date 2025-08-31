import marshmallow

class TextSchema(marshmallow.Schema):
    text = marshmallow.fields.String(required=True, metadata={"description": "Texto a analizar."})
    path = marshmallow.fields.String(required=True, metadata={"description": "Ruta asociada al texto."})
    id = marshmallow.fields.String(required=False, metadata={"description": "Identificador opcional del texto."})

class ScarcityRequestSchema(marshmallow.Schema):
    version = marshmallow.fields.String(required=True, metadata={"description": "Versión del esquema."})
    texts = marshmallow.fields.List(marshmallow.fields.Nested(TextSchema), required=True)

class ScarcityInstanceSchema(marshmallow.Schema):
    text = marshmallow.fields.String(required=True)
    path = marshmallow.fields.String(required=True)
    id = marshmallow.fields.String(required=False)
    has_scarcity = marshmallow.fields.Boolean(required=True)

class ScarcityResponseSchema(marshmallow.Schema):
    version = marshmallow.fields.String(required=True)
    instances = marshmallow.fields.List(marshmallow.fields.Nested(ScarcityInstanceSchema), required=True)

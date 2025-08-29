import marshmallow

class ScarcityTokenSchema(marshmallow.Schema):
    text = marshmallow.fields.String(required=True, metadata={"description": "Texto a analizar."})
    path = marshmallow.fields.String(required=True, metadata={"description": "Ruta asociada al texto."})
    id = marshmallow.fields.String(required=False, metadata={"description": "Identificador opcional del texto."})

class ScarcityRequestSchema(marshmallow.Schema):
    Version = marshmallow.fields.String(required=True, metadata={"description": "Versión del esquema."})
    tokens = marshmallow.fields.List(marshmallow.fields.Nested(ScarcityTokenSchema), required=True)

class ScarcityInstance(marshmallow.Schema):
    text = marshmallow.fields.String(required=True)
    path = marshmallow.fields.String(required=True)
    pattern = marshmallow.fields.String(required=True)
    id = marshmallow.fields.String(required=False)

class ScarcityResponseSchema(marshmallow.Schema):
    Version = marshmallow.fields.String(required=True)
    ScarcityInstances = marshmallow.fields.List(marshmallow.fields.Nested(ScarcityInstance), required=True)

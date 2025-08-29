import marshmallow

class UrgencyTokenSchema(marshmallow.Schema):
    text = marshmallow.fields.String(required=True, metadata={"description": "Texto a analizar."})
    path = marshmallow.fields.String(required=True, metadata={"description": "Ruta asociada al texto."})
    id = marshmallow.fields.String(required=False, metadata={"description": "Identificador opcional del texto."})

class UrgencyRequestSchema(marshmallow.Schema):
    Version = marshmallow.fields.String(required=True, metadata={"description": "Versión del esquema."})
    tokens = marshmallow.fields.List(marshmallow.fields.Nested(UrgencyTokenSchema), required=True)

class UrgencyInstance(marshmallow.Schema):
    text = marshmallow.fields.String(required=True)
    path = marshmallow.fields.String(required=True)
    pattern = marshmallow.fields.String(required=True)
    id = marshmallow.fields.String(required=False)

class UrgencyResponseSchema(marshmallow.Schema):
    Version = marshmallow.fields.String(required=True)
    UrgencyInstances = marshmallow.fields.List(marshmallow.fields.Nested(UrgencyInstance), required=True)

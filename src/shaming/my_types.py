import marshmallow


class ShamingTextSchema(marshmallow.Schema):
    ID = marshmallow.fields.String(required=True, metadata={"description": "Unique identifier for the text."})
    Text = marshmallow.fields.String(required=True, metadata={"description": "The text related to the shaming incident."})

class ShamingButtonSchema(marshmallow.Schema):
    ID = marshmallow.fields.String(required=True, metadata={"description": "Unique identifier for the button."})
    Label = marshmallow.fields.String(required=True, metadata={"description": "The label of the button."})

class ShamingSchema(marshmallow.Schema):
    Version = marshmallow.fields.String(
        required=True, metadata={"description": "Version of the schema."}
    )
    Title = marshmallow.fields.String(required=True, metadata={"description": "The title of the shaming incident."})
    Texts = marshmallow.fields.List(
        marshmallow.fields.Nested(ShamingTextSchema),
        required=True,
        metadata={"description": "List of texts (with IDs) related to the shaming incident."},
    )
    Buttons = marshmallow.fields.List(
        marshmallow.fields.Nested(ShamingButtonSchema),
        required=True,
        metadata={"description": "List of buttons (with IDs) related to the shaming incident."},
    )
    Path = marshmallow.fields.String(required=True, metadata={"description": "The path or context associated with the shaming incident."})


class ShamingInstance(marshmallow.Schema):
    """
    Schema for a single shaming instance.
    """
    Text = marshmallow.fields.String(required=True, metadata={"description": "The text of the shaming incident."})
    HasShaming = marshmallow.fields.Boolean(
        required=True, metadata={"description": "Indicates if the text contains shaming."}
    )
    ID = marshmallow.fields.String(
        required=True, metadata={"description": "Unique identifier for the shaming instance."}
    )

class ShamingResponse(marshmallow.Schema):
    """
    Schema for the response containing shaming instances.
    """
    Version = marshmallow.fields.String(
        required=True, metadata={"description": "Version of the schema."}
    )
    Title = marshmallow.fields.Nested(ShamingInstance, required=True, metadata={"description": "The title of the shaming response."})
    ShamingInstances = marshmallow.fields.List(
        marshmallow.fields.Nested(ShamingInstance),
        required=True,
        metadata={"description": "List of shaming instances."},
    )
    Path = marshmallow.fields.String(required=True, metadata={"description": "The path or context associated with the shaming incidents."})
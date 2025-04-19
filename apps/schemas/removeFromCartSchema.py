from marshmallow import Schema, fields

class RemoveFromCartSchema(Schema):
    user_id=fields.String(required=True,allow_none=False)
    products=fields.List(fields.String, required=True)
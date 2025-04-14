from marshmallow import Schema, fields, validate, EXCLUDE, post_load
from marshmallow.exceptions import ValidationError
from apps.models.cart import Cart


class CartSchema(Schema):
    cart_id = fields.UUID()
    user_id = fields.String(required=True, validate=validate.Length(min=1), allow_none=False)
    product_id = fields.UUID(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    unit_price = fields.Decimal(as_string=True, required=True)
    subtotal = fields.Decimal(as_string=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class CartItemUpdateSchema(Schema):
    quantity = fields.Int(required=True, validate=validate.Range(min=1))


from marshmallow import Schema, fields
from collections import OrderedDict
from marshmallow import Schema, fields,  validates, ValidationError, validate, validates_schema, post_dump

class OrderItemSchema(Schema):
    product_id = fields.UUID(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1, error="Quantity must be at least 1."))
    unit_price = fields.Float(required=True, validate=validate.Range(min=0, error="Price cannot be negative."))

class OrderHistoryDtoSchema(Schema):
    order_id = fields.UUID()
    user_id = fields.String()
    order_status = fields.String()
    shipping_address=fields.String()
    order_items = fields.Nested(OrderItemSchema, many=True, required=True)
    total_amount = fields.Float(required=True,  validate=validate.Range(min=0, error="Total amount cannot be negative."))

orders_History_dto_schema = OrderHistoryDtoSchema()
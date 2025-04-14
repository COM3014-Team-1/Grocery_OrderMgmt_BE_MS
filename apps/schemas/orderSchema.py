from marshmallow import Schema, fields,  validates, ValidationError, validate, validates_schema

class OrderItemSchema(Schema):
    product_id = fields.UUID(required=True)
    quantity = fields.Integer(required=True, validate=validate.Range(min=1, error="Quantity must be at least 1."))
    unit_price = fields.Float(required=True, validate=validate.Range(min=0, error="Price cannot be negative."))

class OrderSchema(Schema):
    user_id = fields.String(required=True)
    total_amount = fields.Float(required=True,  validate=validate.Range(min=0, error="Total amount cannot be negative."))
    order_items = fields.Nested(OrderItemSchema, many=True, required=True)
    order_id = fields.UUID()
    order_status = fields.String(required=False, validate=validate.OneOf(["pending", "shipped", "delivered", "cancelled"])) 
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
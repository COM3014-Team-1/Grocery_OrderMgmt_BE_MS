from marshmallow import Schema, fields

class OrderHistoryDtoSchema(Schema):
    order_id = fields.UUID()
    user_id = fields.UUID()
    order_status = fields.String()
    shipping_address=fields.String()

orders_History_dto_schema = OrderHistoryDtoSchema()
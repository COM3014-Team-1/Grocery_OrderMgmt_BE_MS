from app.utils.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

class OrderItem(db.Model):
    __tablename__ = 'order_product'

    order_item_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.order_id'), nullable=False)
    product_id = db.Column(UUID(as_uuid=True), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    create_date = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_date = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
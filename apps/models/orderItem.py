from apps.utils.db import db
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime, timezone

class OrderItems(db.Model):
    __tablename__ = 'order_items'

    order_item_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = db.Column(UUID(as_uuid=True), db.ForeignKey('orders.order_id'), nullable=False)
    user_id = db.Column(db.String(50), nullable=True)
    product_id = db.Column(UUID(as_uuid=True), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    create_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    
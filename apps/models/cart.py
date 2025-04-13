from datetime import datetime, timezone
from apps.utils.db import db
import uuid
from sqlalchemy.dialects.postgresql import UUID

class Cart(db.Model):
    __tablename__ = 'cart'

    cart_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)  
    user_id = db.Column(db.String(50), nullable=False) 
    product_id = db.Column(UUID(as_uuid=True), nullable=False)  
    quantity = db.Column(db.Integer, default=1, nullable=False) 
    unit_price = db.Column(db.Float(10, 2), nullable=False) 
    subtotal = db.Column(db.Float(10, 2))
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc)) 
    updated_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    def __init__(self, user_id, product_id, quantity, unit_price):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = quantity * unit_price

    def serialize(self):
        """Serialize cart object to dictionary for response"""
        return {
            "cart_id": self.cart_id,
            "user_id": self.user_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": str(self.unit_price),
            "subtotal": str(self.subtotal),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

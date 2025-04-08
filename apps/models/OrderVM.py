from apps.models import OrderProductVM

class OrderVM:
    def __init__(self, order):
        self.order_id = str(order.order_id)
        self.user_id = str(order.user_id)
        self.total_amount = order.total_amount
        self.order_status = order.order_status
        self.created_at = order.created_at.isoformat() if order.created_at else None
        self.updated_at = order.updated_at.isoformat() if order.updated_date else None
        self.order_products = [OrderProductVM(order_product).to_dict() for order_product in order.order._products] if order.order_products else []
    
    def to_dict(self):
        """Convert OrderVM to a dictionary"""
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "total_amount": self.total_amount,
            "order_status": self.order_status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "order_products": self.order_products
        }

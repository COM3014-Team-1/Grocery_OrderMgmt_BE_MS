class OrderVM:
    def __init__(self, order):
        self.order_id = order.order_id
        self.user_id = order.user_id
        self.total_amount = order.total_amount
        self.order_status = order.order_status
        self.created_at = order.created_at.isoformat()  
        self.updated_date = order.updated_date.isoformat()
    
    def to_dict(self):
        """Convert OrderVM to a dictionary"""
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "total_amount": self.total_amount,
            "order_status": self.order_status,
            "created_at": self.created_at,
            "updated_date": self.updated_date
        }

class OrderProductVM:
    def __init__(self, order_item):
        self.order_item_id = str(order_item.order_item_id)
        self.order_id = str(order_item.order_id)
        self.product_id = str(order_item.product_id)
        self.user_id=str(order_item.user_id)
        self.quantity = order_item.quantity
        self.unit_price = order_item.price
    
    def to_dict(self):
        """Convert OrderProductVM to a dictionary"""
        return {
            "order_product_id": str(self.order_item_id) ,
            "order_id": str(self.order_id),
            "product_id": self.product_id,
            "user_id" : self.user_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price
        }

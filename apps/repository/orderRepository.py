from apps.models.order import Order
from apps.models.orderItem import OrderItems
from apps.utils.db import db
from sqlalchemy.orm import joinedload
from datetime import datetime, timezone
from flask import current_app
from apps.utils.validators import validator

class OrderRepository:
    def __init__(self, session=db.session):
        self.session = session

    def create_order(self, data):
        try:
            order = Order(user_id=data['user_id'], total_amount=data['total_amount'])
            self.session.add(order)
            self.session.commit()

            for product in data['order_items']:
                order_product = OrderItems(order_id=order.order_id, product_id=product['product_id'],
                                             quantity=product['quantity'], unit_price=product['unit_price'])
                self.session.add(order_product)

            self.session.commit()
            current_app.logger.info(f"Order has been created with orderId: {order.order_id}")
            return order
        except Exception as err:
            current_app.logger.error(f"Error creating order in repository: {str(err)}")
            raise

    def update_order(self, order_id, data):
        try:
            order = Order.query.get(order_id)
            if not order:
                return None
            if 'order_status' in data:
                order.order_status = data['order_status']
            order.updated_date = datetime.now(timezone.utc)
            self.session.commit()
            return order
        except Exception as err:
            current_app.logger.error(f"Error updating order {order_id} in repository: {str(err)}")
            raise

    def cancel_order(self, order_id):
        try:
            order = Order.query.get(order_id)
            if not order or order.order_status == "Cancelled":
                return None
            order.order_status = "Cancelled"
            order.updated_date = datetime.now(timezone.utc)
            self.session.commit()
            current_app.logger.info(f"Order with id: {order.order_id} has been Cancelled")
            return order
        except Exception as err:
            current_app.logger.error(f"Error cancelling order {order_id} in repository: {str(err)}")
            raise

    def get_order(self, order_id):
        try:
            return Order.query.options(joinedload(Order.order_items)).get(order_id)
        except Exception as err:
            current_app.logger.error(f"Error fetching order {order_id} in repository: {str(err)}")
            raise

    def get_user_orders(self, user_id):
        try:
            return Order.query.filter_by(user_id=user_id).options(joinedload(Order.order_items)).all()
        except Exception as err:
            current_app.logger.error(f"Error fetching orders for user {user_id} in repository: {str(err)}")
            raise
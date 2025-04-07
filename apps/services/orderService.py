from apps.exception.exception import OrderNotFoundError, OrderCreationError, OrderUpdateError, OrderCancelError ,UserOrdersFetchError
from apps.repository.orderRepository import OrderRepository
from marshmallow import ValidationError
from apps.utils.validators import validator 
from flask import current_app
from apps.models.order import Order
from apps.models.orderItem import OrderProduct
from apps.utils.util import util

class OrderService:
    def __init__(self, order_repository=None):
        self.order_repository = order_repository or OrderRepository()

    def create_order(self, data):
        try:
            order = self.order_repository.create_order(data)
            return order
        except ValidationError as err:
            current_app.logger.error(f"Validation error: {err}")
            raise OrderCreationError("Invalid data provided for order creation.")
        except Exception as err:
            current_app.logger.error(f"Error creating order: {str(err)}")
            raise OrderCreationError(f"Error creating order: {str(err)}")

    def update_order(self, order_id, data):
        try:
            validator.validate_Update_fields(data)
            order = self.order_repository.update_order(order_id, data)
            if not order:
                raise OrderNotFoundError(f"Order with ID {order_id} not found.")
            return order
        except ValidationError as err:
            current_app.logger.error(f"Validation error: {err}")
            raise OrderUpdateError("Invalid status or data provided for order update.")
        except OrderNotFoundError as err:
            raise
        except Exception as err:
            current_app.logger.error(f"Error updating order with id {order_id}: {str(err)}")
            raise OrderUpdateError(f"Error updating order with id {order_id}: {str(err)}")

    def cancel_order(self, order_id):
        try:
            order = self.order_repository.cancel_order(order_id)
            if not order:
                raise OrderNotFoundError(f"Order with ID {order_id} not found or already cancelled.")
            return order
        except OrderNotFoundError as err:
            raise
        except Exception as err:
            current_app.logger.error(f"Error canceling order with id {order_id}: {str(err)}")
            raise OrderCancelError(f"Error canceling order with id {order_id}: {str(err)}")

    def get_order(self, order_id):
        try:
            order = self.order_repository.get_order(order_id)
            if not order:
                raise OrderNotFoundError(f"Order with ID {order_id} not found.")
            return order
        except OrderNotFoundError as err:
            raise
        except Exception as err:
            current_app.logger.error(f"Error fetching order with id {order_id}: {str(err)}")
            raise OrderNotFoundError(f"Error fetching order with id {order_id}: {str(err)}")

    def get_user_orders(self, user_id):
        try:
            orders = self.order_repository.get_user_orders(user_id)
            if not orders:
                raise UserOrdersFetchError(f"No orders found for user with ID {user_id}.")
            return orders
        except UserOrdersFetchError as err:
            raise
        except Exception as err:
            current_app.logger.error(f"Error fetching orders for user with id {user_id}: {str(err)}")
            raise UserOrdersFetchError(f"Error fetching orders for user with id {user_id}: {str(err)}")

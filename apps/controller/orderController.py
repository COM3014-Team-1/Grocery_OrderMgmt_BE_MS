from flask import Blueprint, request, jsonify, current_app
from apps.services.orderService import OrderService
from apps.schemas.orderSchema import order_schema, orders_schema
from apps.schemas.orderHistoryDto import orders_History_dto_schema
from marshmallow import ValidationError
from apps.exception.exception import OrderNotFoundError, OrderCreationError, OrderUpdateError, OrderCancelError, UserOrdersFetchError
from apps.utils.errorHandler import ErrorHandlerUtil
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('order', __name__)
order_service = OrderService()

@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order_controller():
    try:
        data = order_schema.load(request.get_json())  
        current_app.logger.info("Creating Order")
        order = order_service.create_order(data)
        return jsonify({"message": f"Order Created Successfully with OrderId: {order.order_id}"}), 201
    except ValidationError as err:
        return ErrorHandlerUtil.handle_validation_error(err)
    except OrderCreationError as err:
        return ErrorHandlerUtil.handle_custom_error(err)
    except Exception as err:
        return ErrorHandlerUtil.handle_generic_error(err)

@order_bp.route('/orders/<order_id>', methods=['PUT'])
@jwt_required()
def update_order_status_controller(order_id):
    try:
        data = order_schema.load(request.get_json(), partial=True)
        current_app.logger.info(f"Updating Order with id: {order_id}")
        order = order_service.update_order(order_id, data)
        if order:
            return jsonify({"message": f"Order with id: {order.order_id} Updated with status: {order.order_status}"}), 200
        return ErrorHandlerUtil.handle_not_found_error("Order not found with id: {}".format(order_id))
    except ValidationError as err:
        return ErrorHandlerUtil.handle_validation_error(err)
    except OrderUpdateError as err:
        return ErrorHandlerUtil.handle_custom_error(err)
    except Exception as err:
        return ErrorHandlerUtil.handle_generic_error(err)

@order_bp.route('/orders/<order_id>', methods=['DELETE'])
@jwt_required()
def cancel_order_controller(order_id):
    try:
        order = order_service.cancel_order(order_id)
        if order:
            return jsonify({'message': 'Order cancelled'}), 200
        return ErrorHandlerUtil.handle_not_found_error("Order not found or already cancelled with id: {}".format(order_id))
    except OrderCancelError as err:
        return ErrorHandlerUtil.handle_custom_error(err)
    except Exception as err:
        return ErrorHandlerUtil.handle_generic_error(err)

@order_bp.route('/orders/<order_id>', methods=['GET'])
@jwt_required()
def order_history_controller(order_id):
    try:
        order = order_service.get_order(order_id)
        if order:
            return jsonify(orders_History_dto_schema.dump(order)), 200
        return ErrorHandlerUtil.handle_not_found_error("Order not found with id: {}".format(order_id))
    except OrderNotFoundError as err:
        return ErrorHandlerUtil.handle_custom_error(err)
    except Exception as err:
        return ErrorHandlerUtil.handle_generic_error(err)

@order_bp.route('/users/<user_id>/orders', methods=['GET'])
@jwt_required()
def get_user_orders_controller(user_id):
    try:
        orders = order_service.get_user_orders(user_id)
        return jsonify(orders_schema.dump(orders)), 200
    except UserOrdersFetchError as err:
        return ErrorHandlerUtil.handle_custom_error(err)
    except Exception as err:
        return ErrorHandlerUtil.handle_generic_error(err)

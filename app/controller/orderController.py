from flask import request,jsonify, current_app
from app.services.orderService import update_order, cancel_order, get_order
from app.models import OrderItemVM, OrderVM


def update_order_controller(order_id):
    try:
        data = request.get_json()
        order = update_order(order_id, data)
        if order:
            order_vm = OrderVM(order)
            return jsonify(order_vm.to_dict()), 200
        return jsonify({'message': 'Order not found'}), 404
    except Exception as err:
        current_app.logger.error(f"Error updating order: {err}")
        return jsonify({"message": "Error updating order"}), 500

def cancel_order_controller(order_id):
    order = cancel_order(order_id)
    if order:
        order_vm = OrderVM(order)
        return jsonify(order_vm.to_dict()), 200
    return jsonify({'message': 'Order not found or already cancelled'}), 404

def order_history_controller(order_id):
    order = get_order(order_id)
    if order:
        order_vm = OrderVM(order)
        return jsonify(order_vm.to_dict()), 200
    return jsonify({'message': 'Order not found'}), 404


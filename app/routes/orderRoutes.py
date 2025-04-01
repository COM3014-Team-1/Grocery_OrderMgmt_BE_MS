from flask import Blueprint
from app.controller.orderController import  update_order_controller, cancel_order_controller, order_history_controller

order_bp = Blueprint('order', __name__)

order_bp.route('/orders/<order_id>', methods=['PUT'])(update_order_controller)
order_bp.route('/orders/<order_id>', methods=['DELETE'])(cancel_order_controller)
order_bp.route('/orders/<order_id>', methods=['GET'])(order_history_controller)

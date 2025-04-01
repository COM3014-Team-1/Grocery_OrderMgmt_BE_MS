from app.models.order import Order
from app.models.orderItem import OrderItem
from app.utils.db import db
from sqlalchemy.orm import joinedload
from datetime import datetime, timezone
from flask import current_app

def create_order(data):
    order = Order(user_id=data['user_id'], total_amount=data['total_amount'])
    db.session.add(order)
    db.session.commit()
    
    for product in data['order_products']:
        order_Item = OrderItem(order_id=order.order_id, product_id=product['product_id'], quantity=product['quantity'], price=product['price'])
        db.session.add(order_Item)

    db.session.commit()
    current_app.logger.info("Order has been created with orderId: {}".format(order.order_id))
    return order

def update_order(order_id, data):
    order = Order.query.get(order_id)
    if not order:
        return None
    if 'order_status' in data:
        order.order_status = data['order_status']

    order.updated_date = datetime.now(timezone.utc)
    db.session.commit()
    current_app.logger.info("Order with id: {} has been Updated with status: {}".format(order.order_id,order.order_status))
    return order

def cancel_order(order_id):
    order = Order.query.get(order_id)
    if not order or order.order_status == "Cancelled":
        return None
    
    order.order_status = "Cancelled"
    order.updated_date = datetime.now(timezone.utc)
    db.session.commit()
    current_app.logger.info("Order with id: {} has been Cancelled".format(order.order_id))
    return order

def get_order(order_id):
    current_app.logger.info("Fetching OrderId: {} from DB".format(order_id))
    return Order.query.options(joinedload(Order.order_products)).get(order_id)

def get_user_orders(user_id):
    current_app.logger.info("Fetching All orders for UserId: {} from DB".format(user_id))
    return Order.query.filter_by(user_id=user_id).options(joinedload(Order.order_products)).all()

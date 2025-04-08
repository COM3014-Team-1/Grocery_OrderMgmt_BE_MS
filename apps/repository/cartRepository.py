from apps.models.cart import Cart
from apps.utils.db import db
from flask import current_app

class CartRepository:
    def __init__(self, session=db.session):
        self.session = session

    def add_product_to_cart(self, user_id, order_id, product_id, quantity, unit_price):
        try:
            cart_item = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
            if cart_item:
                cart_item.quantity += quantity
                cart_item.subtotal = cart_item.quantity * cart_item.unit_price
            else:
                cart_item = Cart(user_id=user_id, order_id=order_id, product_id=product_id, quantity=quantity, unit_price=unit_price)
                db.session.add(cart_item)
                
            db.session.commit()
            current_app.logger.info(f"Product {product_id} added to the cart for user {user_id}")
            return cart_item
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error adding product to cart: {str(e)}")
            raise

    def remove_product_from_cart(self, cart_id):
        try:
            cart_item = Cart.query.get(cart_id)
            if not cart_item:
                return None
            db.session.delete(cart_item)
            db.session.commit()
            current_app.logger.info(f"Product removed from cart: {cart_id}")
            return cart_item
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error removing product from cart: {str(e)}")
            raise

    def update_cart_quantity(self, cart_id, new_quantity):
        try:
            cart_item = Cart.query.get(cart_id)
            if not cart_item:
                return None
            cart_item.quantity = new_quantity
            cart_item.subtotal = cart_item.quantity * cart_item.unit_price
            db.session.commit()
            current_app.logger.info(f"Cart item {cart_id} updated with new quantity {new_quantity}")
            return cart_item
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating cart quantity: {str(e)}")
            raise

    def get_user_cart(self, user_id):
        try:
            return Cart.query.filter_by(user_id=user_id).all()
        except Exception as e:
            current_app.logger.error(f"Error fetching cart items for user {user_id}: {str(e)}")
            raise

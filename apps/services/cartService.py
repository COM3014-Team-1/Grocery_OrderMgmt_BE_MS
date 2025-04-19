from apps.repository.cartRepository import CartRepository
from flask import current_app
from apps.exception.exception import CartItemNotFoundError, CartAddError, CartRemoveError, CartUpdateError, CartFetchError

class CartService:
    def __init__(self, cart_repository=None):
        self.cart_repository = cart_repository or CartRepository()

    def add_to_cart(self, user_id, product_id, quantity, unit_price):
        try:
            cart_item = self.cart_repository.add_product_to_cart(user_id, product_id, quantity, unit_price)
            return cart_item
        except Exception as e:
            current_app.logger.error(f"Error adding to cart: {str(e)}")
            raise CartAddError(f"Error adding product to cart: {str(e)}")

    def remove_from_cart(self, user_id,products):
        current_app.logger.info("Removing items from cart for userId:"+user_id)
        try:
            for productId in products:
                product=self.cart_repository.remove_product_from_cart(user_id,productId)
                if not product:
                    raise CartItemNotFoundError(f"product item with ID {productId} not found.")
            return products                
        except CartItemNotFoundError as e:
            raise 
        except Exception as e:
            current_app.logger.error(f"Error removing from cart: {str(e)}")
            raise CartRemoveError(f"Error removing cart item: {str(e)}")

    def update_cart(self, product_id, new_quantity):
        try:
            cart_item = self.cart_repository.update_cart_quantity(product_id, new_quantity)
            if not cart_item:
                raise CartItemNotFoundError(f"Cart item with ID {product_id} not found.")
            return cart_item
        except CartItemNotFoundError as e:
            raise
        except Exception as e:
            current_app.logger.error(f"Error updating cart: {str(e)}")
            raise CartUpdateError(f"Error updating cart item: {str(e)}")

    def get_user_cart(self, user_id):
        try:
            cart_items = self.cart_repository.get_user_cart(user_id)
            if not cart_items:
                raise CartFetchError(f"No cart items found for user {user_id}.")
            return cart_items
        except CartFetchError as e:
            raise
        except Exception as e:
            current_app.logger.error(f"Error fetching cart items for user {user_id}: {str(e)}")
            raise CartFetchError(f"Error fetching cart items for user {user_id}: {str(e)}")

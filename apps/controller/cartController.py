from flask import Blueprint, request, jsonify, current_app
from apps.services.cartService import CartService
from apps.schemas.cartSchema import CartSchema, CartItemUpdateSchema
from marshmallow import ValidationError
from apps.utils.errorHandler import ErrorHandlerUtil
from apps.utils.logger import LoggerUtil
from apps.exception.exception import CartItemNotFoundError, CartAddError, CartRemoveError, CartUpdateError, CartFetchError

cart_bp = Blueprint('cart', __name__)

cart_service = CartService()

@cart_bp.route('/cart/<string:user_id>', methods=['GET'])
def get_cart(user_id):
    try:
        LoggerUtil.log_info(f"Fetching cart for userId: {str(user_id)}")
        cart_items = cart_service.get_user_cart(user_id)
        return jsonify([CartSchema().dump(item) for item in cart_items]), 200
    except CartFetchError as e:
        return ErrorHandlerUtil.handle_custom_error(e)
    except Exception as e:
        return ErrorHandlerUtil.handle_generic_error(e)

@cart_bp.route('/cart', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        schema = CartSchema()
        validated_data = schema.load(data)
        
        user_id = validated_data['user_id']
        product_id = validated_data['product_id']
        quantity = validated_data['quantity']
        unit_price = validated_data['unit_price'] 
        cart_item = cart_service.add_to_cart(user_id, product_id, quantity, unit_price)
        return jsonify(schema.dump(cart_item)), 201
    except ValidationError as err:
        return ErrorHandlerUtil.handle_validation_error(err)
    except CartAddError as e:
        return ErrorHandlerUtil.handle_custom_error(e)
    except Exception as e:
        return ErrorHandlerUtil.handle_generic_error(e)

@cart_bp.route('/cart/<uuid:cart_id>', methods=['DELETE'])
def remove_from_cart(cart_id):
    try:
        cart_item = cart_service.remove_from_cart(cart_id)
        return jsonify({"message": "Cart item removed successfully"}), 200
    except CartItemNotFoundError:
        return ErrorHandlerUtil.handle_cart_item_not_found_error("Cart item with id: {} not found".format(cart_id))
    except CartRemoveError as e:
        return ErrorHandlerUtil.handle_custom_error(e)
    except Exception as e:
        return ErrorHandlerUtil.handle_generic_error(e)

@cart_bp.route('/cart/<uuid:cart_id>', methods=['PUT'])
def update_cart(cart_id):
    try:
        data = request.get_json()
        schema = CartItemUpdateSchema()
        validated_data = schema.load(data)
        
        new_quantity = validated_data['quantity']
        cart_item = cart_service.update_cart(cart_id, new_quantity)
        
        return jsonify(CartSchema().dump(cart_item)), 200
    except ValidationError as err:
        return ErrorHandlerUtil.handle_validation_error(err)
    except CartItemNotFoundError:
        return ErrorHandlerUtil.handle_cart_item_not_found_error("Updated failed Cart item with id: {} not found".format(cart_id))
    except CartUpdateError as e:
        return ErrorHandlerUtil.handle_custom_error(e)
    except Exception as e:
        return ErrorHandlerUtil.handle_generic_error(e)

from flask import Blueprint, request, jsonify, current_app
from apps.services.cartService import CartService
from apps.schemas.cartSchema import CartSchema, CartItemUpdateSchema
from apps.schemas.removeFromCartSchema import RemoveFromCartSchema
from marshmallow import ValidationError
from apps.utils.errorHandler import ErrorHandlerUtil
from apps.utils.logger import LoggerUtil
from apps.exception.exception import CartItemNotFoundError, CartAddError, CartRemoveError, CartUpdateError, CartFetchError
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.utils.authDecorator import role_required
from apps.schemas.responseSchema import Response

cart_bp = Blueprint('cart', __name__)

cart_service = CartService()

@cart_bp.route('/cart/<string:user_id>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'user'])
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
@jwt_required()
@role_required(['admin', 'user'])
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

@cart_bp.route('/cartItems', methods=['DELETE'])
@jwt_required()
@role_required(['admin', 'user'])
def remove_from_cart():
    try:
        data= request.get_json()
        removeItem=RemoveFromCartSchema().load(data)
        cart_service.remove_from_cart(removeItem['user_id'],removeItem['products'])
        response=Response("Cart item removed successfully",removeItem['products'])
        return jsonify(response.to_dict()), 200
    except CartItemNotFoundError as e:
        return ErrorHandlerUtil.handle_cart_item_not_found_error(e)
    except CartRemoveError as e:
        return ErrorHandlerUtil.handle_custom_error(e)
    except Exception as e:
        return ErrorHandlerUtil.handle_generic_error(e)

@cart_bp.route('/cart/<string:product_id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'user'])
def update_cart(product_id):
    try:
        data = request.get_json()
        schema = CartItemUpdateSchema()
        validated_data = schema.load(data)
        new_quantity = validated_data['quantity']
        cart_item = cart_service.update_cart(product_id, new_quantity)
        return jsonify(CartSchema().dump(cart_item)), 200
    except ValidationError as err:
        return ErrorHandlerUtil.handle_validation_error(err)
    except CartItemNotFoundError:
        return ErrorHandlerUtil.handle_cart_item_not_found_error("Updated failed Cart item with id: {} not found".format(product_id))
    except CartUpdateError as e:
        return ErrorHandlerUtil.handle_custom_error(e)
    except Exception as e:
        return ErrorHandlerUtil.handle_generic_error(e)


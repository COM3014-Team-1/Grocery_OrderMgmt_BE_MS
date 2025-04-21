from apps.exception.exception import CartAddError, CartItemNotFoundError, CartUpdateError, CartRemoveError, CartFetchError, ProductAvailabilityError
from flask import jsonify
from apps.utils.logger import LoggerUtil

class ErrorHandlerUtil:
    @staticmethod
    def handle_validation_error(err):
        return jsonify({"errors": err.messages}), 400

    @staticmethod
    def handle_cart_item_not_found_error(error : Exception):
        return jsonify({"error": str(error)}), 404

    @staticmethod
    def handle_custom_error(error: Exception):
        LoggerUtil.log_error("Custom Error", error)
        return jsonify({"error": str(error)}), 500

    @staticmethod
    def handle_generic_error(error: Exception):
        LoggerUtil.log_error("Unexpected Error", error)
        return jsonify({"error": str(error)}), 500
    
    @staticmethod
    def handle_not_found_error(message):
        return jsonify({"error": message}), 404
    
    @staticmethod
    def handle_Produc_unavaliable_error(err):
        return jsonify({
            "error": "ProductAvailabilityError",
            "message": str(err),
            "unavailable_products": err.unavailable_products
        }), 400

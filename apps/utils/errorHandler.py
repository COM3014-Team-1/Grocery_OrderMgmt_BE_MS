from apps.exception.exception import CartAddError, CartItemNotFoundError, CartUpdateError, CartRemoveError, CartFetchError
from flask import jsonify
from apps.utils.logger import LoggerUtil

class ErrorHandlerUtil:
    @staticmethod
    def handle_validation_error(err):
        """ Handles validation errors across controllers """
        return jsonify({"errors": err.messages}), 400

    @staticmethod
    def handle_cart_item_not_found_error(message):
        """ Handle cart item not found error """
        return jsonify({"error": message}), 404

    @staticmethod
    def handle_custom_error(error: Exception):
        """ Handle custom errors, logs, and returns proper response """
        LoggerUtil.log_error("Custom Error", error)

        return jsonify({"error": str(error)}), 500

    @staticmethod
    def handle_generic_error(error: Exception):
        """ Handle unexpected errors """
        LoggerUtil.log_error("Unexpected Error", error)
        return jsonify({"error": str(error)}), 500
    
    @staticmethod
    def handle_not_found_error(message):
        """Handles not found errors (404)"""
        return jsonify({"error": message}), 404

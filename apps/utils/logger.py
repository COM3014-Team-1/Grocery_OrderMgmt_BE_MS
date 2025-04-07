import logging
from flask import current_app

class LoggerUtil:
    @staticmethod
    def log_error(message: str, error: Exception):
        """ Log error messages with the exception details """
        current_app.logger.error(f"{message}: {str(error)}")

    @staticmethod
    def log_info(message: str):
        """ Log informational messages """
        current_app.logger.info(message)
        
    @staticmethod
    def log_warning(message: str):
        """ Log warning messages """
        current_app.logger.warning(message)

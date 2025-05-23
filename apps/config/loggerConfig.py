import logging

def configure_logger(app):
    """Configures the logger for the Flask app."""
    logger = logging.getLogger(__name__)  
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

   
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    
    app.logger = logger
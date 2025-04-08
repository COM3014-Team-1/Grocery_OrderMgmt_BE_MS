from flask import Flask
from apps.utils.db import db, init_db
from config import appsettings, Config
from flask_migrate import Migrate
from apps.config.loggerConfig import configure_logger
from apps.config.swaggerConfig import setup_swagger
from apps.controller.cartController import cart_bp
from apps.controller.orderController import order_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    migrate = Migrate(app, db) 
    
    configure_logger(app)
    setup_swagger(app)

    app.register_blueprint(order_bp)
    app.register_blueprint(cart_bp) 

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host=app.config["HOST"], port=app.config["PORT"], debug=True)
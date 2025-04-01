from flask import Flask
from app.utils.db import db, init_db
from config import Config
from flask_migrate import Migrate
from app.routes.orderRoutes import order_bp
from sqlalchemy import inspect

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)
    migrate = Migrate(app, db) 
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.register_blueprint(order_bp)
    app.run(debug=True)
from flask import Flask

from app.database import Database

# Import models
from app.model.product_model import ProductModel
from app.model.user_model import UserModel
from app.model.cart_model import CartModel
from app.model.order_model import OrderModel
from app.routes.general_routes import general_bp


# Import route blueprints
from app.routes.product_routes import product_bp
from app.routes.user_routes import user_bp
from app.routes.cart_routes import cart_bp
from app.routes.order_routes import order_bp


def create_app():
    app = Flask(__name__)

    # Initialize database
    db = Database()

    # Create tables
    ProductModel(db.cursor).create_table()
    UserModel(db.cursor).create_table()
    CartModel(db.cursor).create_table()
    OrderModel(db.cursor).create_table()

    # Register route blueprints
    app.register_blueprint(product_bp, url_prefix="/api")
    app.register_blueprint(user_bp, url_prefix="/api")
    app.register_blueprint(cart_bp, url_prefix="/api")
    app.register_blueprint(order_bp, url_prefix="/api")
    app.register_blueprint(general_bp)  #Homepage


    return app

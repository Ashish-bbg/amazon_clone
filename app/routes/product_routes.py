# app/routes/product_routes.py
from flask import Blueprint, jsonify, request
from app.database import Database
from app.services.product_service import ProductService
from app.model.product_model import ProductModel

product_bp = Blueprint("product", __name__)

# Initialize DB and service
db = Database()
ProductModel(db.cursor).create_table()
service = ProductService(db.cursor, db.con)

@product_bp.route("/products", methods=["GET"])
def get_products():
    return jsonify(service.get_products())

@product_bp.route("/products/<prod_id>", methods=["GET"])
def get_product(prod_id):
    data = service.get_product_by_id(prod_id)
    if data is None:
        return jsonify({"error": "Product ID not found"}), 404
    elif "error" in data:
        return jsonify(data), 500
    return jsonify(data)

@product_bp.route("/products", methods=["POST"])
def add_product():
    prod_data = request.get_json()

    # Simple required fields check
    required = ["prod_id", "title", "imageurl", "producturl", "reviews", "price",
                "isbestseller", "bought_lastmonth", "category_name", "stars"]
    if not all(k in prod_data for k in required):
        return jsonify({"error": "Missing required fields"}), 400

    result = service.add_new_product(prod_data)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

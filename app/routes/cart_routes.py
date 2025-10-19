from flask import Blueprint, request, jsonify
from app.database import Database
from app.model.cart_model import CartModel
from app.services.cart_service import CartService

cart_bp = Blueprint("cart", __name__)

db = Database()
CartModel(db.cursor).create_table()
cart_service = CartService(db.cursor, db.con)

@cart_bp.route("/cart/<user_id>", methods=["GET"])
def get_cart(user_id):
    data = cart_service.get_cart_by_user(user_id)
    return jsonify(data)

@cart_bp.route("/cart", methods=["POST"])
def add_cart_item():
    data = request.get_json()
    required = ["user_id", "prodid", "quantity"]
    if not all(field in data for field in required):
        return jsonify({"error": "Missing fields"}), 400

    result = cart_service.add_to_cart(data["user_id"], data["prodid"], data["quantity"])
    status = 200 if "success" in result else 500
    return jsonify(result), status

@cart_bp.route("/cart/<int:cartid>", methods=["DELETE"])
def delete_cart_item(cartid):
    result = cart_service.remove_from_cart(cartid)
    status = 200 if "success" in result else 500
    return jsonify(result), status

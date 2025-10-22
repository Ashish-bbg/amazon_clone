# app/routes/order_routes.py

from flask import Blueprint, request, jsonify
from app.database import Database
from app.model.order_model import OrderModel
from app.services.order_service import OrderService

order_bp = Blueprint("order", __name__)

db = Database()
OrderModel(db.cursor).create_table()
order_service = OrderService(db.cursor, db.con)

@order_bp.route("/orders", methods=["POST"])
def checkout():
    data = request.get_json()
    user_id = data.get("user_id")
    total_price = data.get("total_price")

    if not user_id or total_price is None:
        return jsonify({"error": "Missing user_id or total_price"}), 400

    result = order_service.checkout(user_id, total_price)
    status = 200 if "success" in result else 500
    return jsonify(result), status

@order_bp.route("/orders/<user_id>", methods=["GET"])
def get_user_orders(user_id):
    data = order_service.get_orders_by_user(user_id)
    return jsonify(data)

@order_bp.route("/order/<int:order_id>", methods=["GET"])
def get_order_by_id(order_id):
    data = order_service.get_order_by_id(order_id)
    if data:
        return jsonify(data)
    return jsonify({"error": "Order not found"}), 404

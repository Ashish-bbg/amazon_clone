# app/routes/user_routes.py

from flask import Blueprint, jsonify, request
from app.database import Database
from app.model.user_model import UserModel
from app.services.user_service import UserService

user_bp = Blueprint("user", __name__)

# Init DB + table
db = Database()
UserModel(db.cursor).create_table()
user_service = UserService(db.cursor, db.con)

@user_bp.route("/users", methods=["GET"])
def get_users():
    user = user_service.get_users()
    if user:
        return jsonify(user)
    return jsonify({"error": "NO User not found"}), 404

@user_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@user_bp.route("/add_user", methods=["POST"])
def add_user():
    data = request.get_json()
    required = ["user_id", "name", "email", "password_hash", "address"]
    if not all(field in data for field in required):
        return jsonify({"error": "Missing required fields"}), 400

    result = user_service.add_user(data)
    status = 500 if "error" in result else 201
    return jsonify(result), status

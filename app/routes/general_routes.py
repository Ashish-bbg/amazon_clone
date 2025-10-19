from flask import Blueprint, jsonify

general_bp = Blueprint("general", __name__)

@general_bp.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Hi Welcome to the Amazon Clone API!",
        "status": "running",
        "available_endpoints": [
            "/api/products",
            "/api/cart",
            "/api/orders",
            "/api/users"
        ]
    })

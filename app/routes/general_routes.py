from flask import Blueprint, jsonify, request
from app.dataloader import import_excel_to_db

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



@general_bp.route("/import-data", methods=["POST"])
def import_data():
    try:
        # Optional file path from the request body
        data = request.get_json(silent=True) or {}
        file_path = data.get("file_path", "C:/Users/sumit.bz.sharma/OneDrive - Accenture/ML with Python/Amazon_Clone/Dataset/demo_productdata.csv")

        import_excel_to_db(file_path)

        return jsonify({
            "message": f" Data imported successfully from {file_path}",
            "status": "success"
        }), 200

    except Exception as e:
        return jsonify({
            "message": " Failed to import data",
            "error": str(e),
            "status": "error"
        }), 500

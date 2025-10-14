import Python_sql_functions as py
from flask import Flask, jsonify, request
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

conn = py.SQL_Connection()


@app.route("/")
def home():
    return py.SQL_Connection.home()


@app.route("/api/add_to_cart")
def table_description():
    return conn.create_table_products("Cart")


@app.route("/api/products")
def get_products():
    return jsonify(conn.get_products("products"))


@app.route("/api/id=<prod_id>", methods=["GET"])
def get_product_by_id(prod_id):
    data = conn.get_product_by_id(prod_id)
    if "error" in data:
        return jsonify(data), 500
    elif data:
        return jsonify(data)
    else:
        return jsonify({"Error": "Product ID not found!!"}), 404
    
@app.route('/api/add_new', methods=['POST'])
def add_new():
    data = request.get_json()

    # Extract data from the JSON body
    prod_id = data.get('prod_id')
    title = data.get('title')
    imageurl = data.get('imageurl')
    producturl = data.get('producturl')
    reviews = data.get('reviews')
    price = data.get('price')
    isbestseller = data.get('isbestseller')
    bought_lastmonth = data.get('bought_lastmonth')
    category_name = data.get('category_name')
    stars = data.get('stars')
    
    result= conn.add_new_product( prod_id,title, imageurl, producturl, reviews, price, isbestseller, bought_lastmonth, category_name, stars)


    if "Error" in result:
        return jsonify(result), 500
    elif data:
        return jsonify(result)
    else:
        return jsonify({"Alert": "Do enter all the required fields!!"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)

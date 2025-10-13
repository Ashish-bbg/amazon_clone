import Python_sql_functions as py
from flask import Flask,jsonify,request
import os
from dotenv import load_dotenv

load_dotenv()

app=Flask(__name__)

conn=py.SQL_Connection()

@app.route('/')
def home():
    return py.SQL_Connection.home()

@app.route("/api/table_description")
def table_description():
     return conn.create_table_products("demo1")

@app.route('/api/products')
def get_products():
    return jsonify(conn.get_products('products'))

@app.route('/api/id=<prod_id>', methods=['GET'])
def get_product_by_id(prod_id):
    data=conn.get_product_by_id(prod_id)
    if "error" in data:
        return jsonify(data), 500
    elif data:
        return jsonify(data)
    else:
        return jsonify({"Error":"Product ID not found!!"}), 404





if __name__=="__main__":
#     app.run(debug=True)
    app.run(host="0.0.0.0", port=os.getenv("PORT"), debug=True)

# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 4000))  # Railway sets this environment variable
#     app.run(host="0.0.0.0", port=port, debug=True)

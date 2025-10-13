import mysql.connector as sql
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from flask import Flask, jsonify, request


load_dotenv()
db_url = os.getenv("MYSQL_URL")
parsed = urlparse(db_url)
db_config = {
    "host": parsed.hostname,
    "user": parsed.username,
    "password": parsed.password,
    "port": parsed.port or 3306,
}


class SQL_Connection:

    con = sql.connect(**db_config)
    cursor = con.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS amazon_clone;")
    cursor.execute("USE amazon_clone;")
    print("Connected to Railway MySQL!")
    cursor.execute(
        " CREATE TABLE IF NOT EXISTS Products (prodid VARCHAR(10) NOT NULL PRIMARY KEY,title VARCHAR(600),imgurl VARCHAR(500),producturl VARCHAR(500),reviews INT,price FLOAT,isbestseller TINYINT(1),boughtlastmonth  INT,categoryname VARCHAR(100),stars FLOAT);"
    )

    def create_table_products(self, table_name):
        # table_name=self.table_name
        SQL_Connection.cursor.execute(
            f" CREATE TABLE IF NOT EXISTS {table_name} (prodid VARCHAR(10) NOT NULL PRIMARY KEY,title VARCHAR(600),imgurl VARCHAR(500),producturl VARCHAR(500),reviews INT,price FLOAT,isbestseller TINYINT(1),boughtlastmonth  INT,categoryname VARCHAR(100),stars FLOAT);"
        )
        return jsonify({"Success": f"Table {table_name} Created!!"})

    def home():
        return jsonify({"message": "Welcome to AMAZON"})

    def get_products(self, table_name):
        query = f"SELECT * FROM {table_name};"
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        columns = [desc[0] for desc in self.cursor.description]
        data = [dict(zip(columns, row)) for row in rows]
        return data

    def get_product_by_id(self, prod_id):
        try:
            query = f"""Select * from products where prodid="{prod_id}";"""
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            data = [dict(zip(columns, row)) for row in rows]
            return data
        except Exception as e:
            return {"error": str(e)}

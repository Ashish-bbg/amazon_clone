# app/services/product_service.py
class ProductService:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.con = connection

    def get_products(self):
        try:
            self.cursor.execute("SELECT * FROM products;")
            rows = self.cursor.fetchall()
            return (rows) if rows else None
        except Exception as e:
            return {"error": str(e)}

    def get_product_by_id(self, prod_id):
        try:
            self.cursor.execute("SELECT * FROM products WHERE prodid=%s;", (prod_id,))
            rows = self.cursor.fetchall()
            return (rows) if rows else None
        except Exception as e:
            return {"error": str(e)}

    def add_new_product(self, prod_data):
        try:
            query = """
                INSERT INTO products (
                    prodid, title, imgurl, producturl, reviews, price, 
                    isbestseller, boughtlastmonth, categoryname, stars, stock
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            self.cursor.execute(query, (
                prod_data["prod_id"], prod_data["title"], prod_data["imageurl"],
                prod_data["producturl"], prod_data["reviews"], prod_data["price"],
                prod_data["isbestseller"], prod_data["bought_lastmonth"],
                prod_data["category_name"], prod_data["stars"], prod_data["stock"]
            ))
            self.con.commit()
            return {"success": f"Product {prod_data['prod_id']} added successfully!"}
        except Exception as e:
            return {"error": str(e)}

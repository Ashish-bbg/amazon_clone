# app/models/product_model.py
class ProductModel:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                prodid VARCHAR(10) NOT NULL PRIMARY KEY,
                title VARCHAR(600),
                imgurl VARCHAR(500),
                producturl VARCHAR(500),
                reviews INT,
                price FLOAT,
                isbestseller TINYINT(1),
                boughtlastmonth INT,
                categoryname VARCHAR(100),
                stars FLOAT,
                stock INT DEFAULT 10
            );
            """
        )

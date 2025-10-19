# app/model/cart_model.py

class CartModel:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS cart (
                cartid INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(50),
                prodid VARCHAR(10),
                quantity INT DEFAULT 1,
                added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (prodid) REFERENCES products(prodid),
                FOREIGN KEY (user_id) REFERENCES users(user_id),
                UNIQUE (user_id, prodid)
            );
        """)

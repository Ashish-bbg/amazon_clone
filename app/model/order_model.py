# app/model/order_model.py

class OrderModel:
    def __init__(self, cursor):
        self.cursor = cursor

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(50),
                total_price FLOAT,
                status VARCHAR(20) DEFAULT 'Pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        """)

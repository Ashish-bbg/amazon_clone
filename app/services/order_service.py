# app/services/order_service.py

class OrderService:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.con = connection

    def create_order(self, user_id, total_price):
        try:
            self.cursor.execute("""
                INSERT INTO orders (user_id, total_price)
                VALUES (%s, %s)
            """, (user_id, total_price))
            self.con.commit()
            return {"success": "Order created successfully"}
        except Exception as e:
            return {"error": str(e)}

    def get_orders_by_user(self, user_id):
        self.cursor.execute("""
            SELECT * FROM orders WHERE user_id = %s
        """, (user_id,))
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def get_order_by_id(self, order_id):
        self.cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
        row = self.cursor.fetchone()
        if row:
            columns = [desc[0] for desc in self.cursor.description]
            return dict(zip(columns, row))
        return None

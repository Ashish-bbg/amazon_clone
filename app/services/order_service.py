# app/services/order_service.py

class OrderService:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.con = connection

    def checkout(self, user_id, total_price):
        try:
            self.cursor.execute("""
                INSERT INTO orders (user_id, total_price)
                VALUES (%s, %s)
            """, (user_id, total_price))
            #Reducing ordered items from Product table 
            self.cursor.execute("UPDATE products p JOIN cart c on p.prodid = c.prodid set p.stock = p.stock - c.quantity WHERE user_id = %s",(user_id,)) 
            #Empty the cart
            self.cursor.execute("DELETE FROM cart WHERE user_id = %s", (user_id,))

            self.con.commit()
            return {"success": "Order placed successfully"}
        
        except Exception as e:
            return {"error": str(e)}

    def get_orders_by_user(self, user_id):
        try:
            self.cursor.execute("""
                SELECT * FROM orders WHERE user_id = %s
            """, (user_id,))
            rows = self.cursor.fetchall()
            return (rows) if rows else None
        except Exception as e:
            return {"error": str(e)}

    def get_order_by_id(self, order_id):
        try:
            self.cursor.execute("SELECT * FROM orders WHERE order_id = %s", (order_id,))
            rows = self.cursor.fetchone()
            return (rows) if rows else None
        except Exception as e:
            return {"error": str(e)}

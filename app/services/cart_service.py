# app/services/cart_service.py

class CartService:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.con = connection

    def get_cart_by_user(self, user_id):
        self.cursor.execute("""
            SELECT c.cartid, c.quantity, c.added_at, p.title, p.price, p.imgurl 
            FROM cart c 
            JOIN products p ON c.prodid = p.prodid 
            WHERE c.user_id = %s
        """, (user_id,))
        columns = [desc[0] for desc in self.cursor.description]
        return [dict(zip(columns, row)) for row in self.cursor.fetchall()]

    def add_to_cart(self, user_id, prodid, quantity):
        try:
            self.cursor.execute("""
                INSERT INTO cart (user_id, prodid, quantity)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE quantity = quantity + %s;
            """, (user_id, prodid, quantity, quantity))
            self.con.commit()
            return {"success": "Item added to cart"}
        except Exception as e:
            return {"error": str(e)}

    def remove_from_cart(self, cartid):
        try:
            self.cursor.execute("DELETE FROM cart WHERE cartid = %s", (cartid,))
            self.con.commit()
            return {"success": "Item removed from cart"}
        except Exception as e:
            return {"error": str(e)}

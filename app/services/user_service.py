# app/services/user_service.py

class UserService:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.con = connection

    def get_users(self):
        self.cursor.execute("SELECT * FROM users;")
        rows = self.cursor.fetchall()
        if rows:
            return (rows)
        return None

    def get_user_by_id(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        row = self.cursor.fetchone()
        if row:
            columns = [desc[0] for desc in self.cursor.description]
            return dict(zip(columns, row))
        return None

    def add_user(self, user_data):
        try:
            self.cursor.execute("""
                INSERT INTO users (user_id, name, email, password_hash, address)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                user_data["user_id"],
                user_data["name"],
                user_data["email"],
                user_data["password_hash"],
                user_data["address"]
            ))
            self.con.commit()
            return {"success": "User added successfully!"}
        except Exception as e:
            return {"error": str(e)}

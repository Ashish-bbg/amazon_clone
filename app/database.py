import mysql.connector as sql
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        db_url = os.getenv("MYSQL_URL")

        if not db_url:
            print(" MYSQL_URL environment variable not found.")
            self.con = None
            self.cursor = None
            return

        parsed = urlparse(db_url)

        self.config = {
            "host": parsed.hostname,
            "user": parsed.username,
            "password": parsed.password,
            "port": parsed.port or 3306,
        }

        try:
            self.con = sql.connect(**self.config)
            self.cursor = self.con.cursor()
            print(" Successfully connected to MySQL.")

            self._init_database()
        except sql.Error as err:
            print(f" Failed to connect to MySQL: {err}")
            self.con = None
            self.cursor = None

    def _init_database(self):
        try:
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS amazon_clone;")
            self.cursor.execute("USE amazon_clone;")
            print(" Using database: amazon_clone")
        except Exception as e:
            print(f" Failed to initialize database: {e}")

    def commit(self):
        if self.con:
            self.con.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.con:
            self.con.close()

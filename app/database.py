# app/database.py
import mysql.connector as sql
import os
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        db_url = os.getenv("MYSQL_URL")
        parsed = urlparse(db_url)
        self.config = {
            "host": parsed.hostname,
            "user": parsed.username,
            "password": parsed.password,
            "port": parsed.port or 3306,
        }
        self.con = sql.connect(**self.config)
        self.cursor = self.con.cursor()
        self._init_database()

    def _init_database(self):
        self.cursor.execute("CREATE DATABASE IF NOT EXISTS amazon_clone;")
        self.cursor.execute("USE amazon_clone;")
        print("✅ Connected to MySQL and using 'amazon_clone' database.")

    def commit(self):
        self.con.commit()

    def close(self):
        self.cursor.close()
        self.con.close()

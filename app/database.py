import os
from urllib.parse import urlparse
from dotenv import load_dotenv
import mysql.connector as sql
from mysql.connector import pooling, Error

load_dotenv()


class Database:

    _pool = None  # Shared connection pool

    def __init__(self):
        db_url = os.getenv("MYSQL_URL")

        if not db_url:
            print("!! MYSQL_URL environment variable not found.")
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

        # Create a pool only once for the app
        if Database._pool is None:
            try:
                Database._pool = pooling.MySQLConnectionPool(
                    pool_name="mypool",
                    pool_size=5,
                    pool_reset_session=True,
                    **self.config,
                )
                print("✅ MySQL connection pool created.")
            except Error as err:
                print(f"!! Failed to create MySQL connection pool: {err}")
                self.con = None
                self.cursor = None
                return

        # Always get a fresh connection from the pool
        try:
            self.con = Database._pool.get_connection()
            self.cursor = self.con.cursor(dictionary=True)
            print(" Successfully connected to MySQL from pool.")
            self._init_database()
        except Error as err:
            print(f"!! Failed to get MySQL connection: {err}")
            self.con = None
            self.cursor = None

    def _init_database(self):
        # Create and use the amazon_clone database if it doesn’t exist.
        try:
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS amazon_clone;")
            self.cursor.execute("USE amazon_clone;")
            print(" Using database: amazon_clone")
        except Exception as e:
            print(f" Failed to initialize database: {e}")

    def ensure_connection(self):
        # Reconnect if connection is dropped.
        if not self.con:
            print("!!No active connection. Getting new one from pool...")
            self.con = Database._pool.get_connection()
            self.cursor = self.con.cursor(dictionary=True)
            return

        try:
            self.con.ping(reconnect=True, attempts=3, delay=2)
        except Error:
            print("!! Connection lost. Reconnecting...")
            self.con = Database._pool.get_connection()
            self.cursor = self.con.cursor(dictionary=True)

    def commit(self):
        if self.con:
            self.con.commit()

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.con:
            self.con.close()

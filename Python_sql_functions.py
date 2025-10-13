import mysql.connector as sql
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import mysql.connector as sql

load_dotenv()
db_url = os.getenv("MYSQL_URL")
parsed = urlparse(db_url)
db_config = {
    "host": parsed.hostname,
    "user": parsed.username,
    "password": parsed.password,
    "database": parsed.path.lstrip("/"),
    "port": parsed.port or 3306
}

class SQL_Connection():
    
    con = sql.connect(**db_config)
    cursor = con.cursor()
    print("Connected to Railway MySQL!")

    def create_table(self,table_name):
        #table_name=self.table_name
        SQL_Connection.cursor.execute(f""" CREATE TABLE IF NOT EXISTS {table_name} (prodid VARCHAR(10) NOT NULL PRIMARY KEY,title VARCHAR(600),imgurl VARCHAR(500),producturl VARCHAR(500),reviews INT,price FLOAT,isbestseller TINYINT(1),boughtlastmonth  INT,categoryname VARCHAR(100),stars FLOAT);""")
        SQL_Connection.cursor.execute(f"""desc {table_name};""")
        for i in SQL_Connection.cursor:
            print(i)
    
    

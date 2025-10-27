import pandas as pd
from app.database import Database
from app.model import product_model 

def import_excel_to_db(file_path):
    conn = None
    cursor = None
    try:
        # Load Excel file into DataFrame
        df = pd.read_excel(file_path)
        print(f" Loaded {len(df)} rows from Excel file.")

        # Create DB connection
        conn = Database()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO products (
                prodid, title, imgurl, producturl, reviews, price,
                isbestseller, boughtlastmonth, categoryname, stars, stock
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                title = VALUES(title),
                imgurl = VALUES(imgurl),
                producturl = VALUES(producturl),
                reviews = VALUES(reviews),
                price = VALUES(price),
                isbestseller = VALUES(isbestseller),
                boughtlastmonth = VALUES(boughtlastmonth),
                categoryname = VALUES(categoryname),
                stars = VALUES(stars),
                stock = VALUES(stock)
        """

        # Insert data row by row
        for _, row in df.iterrows():
            cursor.execute(insert_query, (
                str(row.get('prodid')),
                row.get('title'),
                row.get('imgurl'),
                row.get('producturl'),
                int(row.get('reviews', 0)) if not pd.isna(row.get('reviews')) else 0,
                float(row.get('price', 0)) if not pd.isna(row.get('price')) else 0.0,
                int(row.get('isbestseller', 0)) if not pd.isna(row.get('isbestseller')) else 0,
                int(row.get('boughtlastmonth', 0)) if not pd.isna(row.get('boughtlastmonth')) else 0,
                row.get('categoryname'),
                float(row.get('stars', 0)) if not pd.isna(row.get('stars')) else 0.0,
                int(row.get('stock', 10)) if not pd.isna(row.get('stock')) else 10
            ))

        # Commit all inserts
        conn.commit()
        print(f" Imported {len(df)} records successfully.")

    except Exception as e:
        print(" Error during import:", e)

    finally:
        # Clean up
        if cursor:
            cursor.close()
        if conn and conn.is_connected():
            conn.close()

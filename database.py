import sqlite3
from typing import List, Dict, Optional, Tuple
import hashlib
import os

def create_database(db_name: str) -> None:
    """
    Creates a SQLite database and a table for storing product information.

    Args:
        db_name (str): The name of the SQLite database file.
    """

    if os.path.exists(db_name):
        print(f"Database '{db_name}' already exists.")
        return

    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Create table with a primary key based on a hash
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            product_title TEXT,
            product_price TEXT,
            product_image_url TEXT
        )
        ''')
        
        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred while creating the database: {e}")
    finally:
        conn.close()

def generate_id(product_title: str, product_price: str, product_image_url: str) -> str:
    """
    Generates a unique ID based on the hash of product_title, product_price, and product_image_url.

    Args:
        product_title (str): The title of the product.
        product_price (str): The price of the product.
        product_image_url (str): The image URL of the product.

    Returns:
        str: A unique hash ID.
    """
    unique_string = f"{product_title}{product_price}{product_image_url}"
    return hashlib.sha256(unique_string.encode()).hexdigest()

def insert_product(db_name: str, product_title: str, product_price: str, product_image_url: str) -> bool:
    """
    Inserts product information into the SQLite database and returns a flag indicating
    whether the product was inserted or already existed.

    Args:
        db_name (str): The name of the SQLite database file.
        product_title (str): The title of the product.
        product_price (str): The price of the product.
        product_image_url (str): The image URL of the product.

    Returns:
        bool: True if the product was inserted, False if it already existed.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        product_id = generate_id(product_title, product_price, product_image_url)
        
        cursor.execute('''
        SELECT COUNT(*) FROM products WHERE id = ?
        ''', (product_id,))
        exists = cursor.fetchone()[0]
        
        if exists == 0:
            cursor.execute('''
            INSERT INTO products (id, product_title, product_price, product_image_url)
            VALUES (?, ?, ?, ?)
            ''', (product_id, product_title, product_price, product_image_url))
            conn.commit()
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(f"An error occurred while inserting a product: {e}")
        return False
    finally:
        conn.close()

def retrieve_products(db_name: str) -> List[Dict[str, str]]:
    """
    Retrieves all products from the SQLite database.

    Args:
        db_name (str): The name of the SQLite database file.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing product information.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, product_title, product_price, product_image_url FROM products')
        products = cursor.fetchall()
        
        return [{'id': row[0], 'product_title': row[1], 'product_price': row[2], 'product_image_url': row[3]} for row in products]
    except sqlite3.Error as e:
        print(f"An error occurred while retrieving products: {e}")
        return []
    finally:
        conn.close()
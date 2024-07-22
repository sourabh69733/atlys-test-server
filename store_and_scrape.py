from scrape_catalogue import scrape_catalogue
from typing import List, Dict, Optional, Tuple
from database import insert_product

def store_and_scrape(db_name: str, url: str, num_pages: int, proxy_string: Optional[str] = None) -> Tuple[List[Dict[str, str]], int, int]:
    products = scrape_catalogue(url, num_pages, proxy_string)
    inserted_count = 0
    existing_count = 0

    try:
        for product_info in products:
            product_title, product_price, product_image_url = product_info.values()
            
            # Insert product into SQLite database and update counts
            if insert_product(db_name, product_title, product_price, product_image_url):
                inserted_count += 1
            else:
                existing_count += 1
    
    except Exception as e:
        print(f"An unexpected error occurred while processing the page: {e}")

    return products, inserted_count, existing_count


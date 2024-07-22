from typing import Union
from fastapi import FastAPI, HTTPException
from database import create_database
from store_and_scrape import store_and_scrape

app = FastAPI()

DATABASE_NAME = 'products.production.db'

def init_db_services() -> bool:
    create_database(DATABASE_NAME)
    return True

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/scrape")
def scrape_catalogue_endpoint(url: str, num_pages: int, proxy: Union[str, None] = None):
    try:
        init_db_services()

        products, inserted_count, existing_count = store_and_scrape(DATABASE_NAME, url, num_pages, proxy_string=proxy)
        return {
            "status": "ok",
            "inserted_count": inserted_count,
            "existing_count": existing_count,
            "total_products": len(products)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to scrape catalogue: {e}")

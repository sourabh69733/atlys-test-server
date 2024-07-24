from typing import Union
from fastapi import FastAPI, HTTPException, Depends, Header
from database import create_database
from store_and_scrape import store_and_scrape

app = FastAPI()

DATABASE_NAME = 'products.production.db'
STATIC_TOKEN = "SERVER_TOKEN"  # Replace with your secure static token

def verify_static_token(token: str = Header(...)) -> None:
    """
    Verifies that the provided token matches the static token.

    Args:
        token (str): The token to verify.

    Raises:`
        HTTPException: If the token is invalid.
    """
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")

def init_db_services() -> bool:
    create_database(DATABASE_NAME)
    return True

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/scrape")
def scrape_catalogue_endpoint(url: str, num_pages: int, proxy: Union[str, None] = None, token: str = Depends(verify_static_token)):
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
        status_code = 500
        # Extract the status code if available
        if e.status_code is not None:
            status_code = e.status_code
        raise HTTPException(status_code=status_code, detail=f"Failed to scrape catalogue: {e}")

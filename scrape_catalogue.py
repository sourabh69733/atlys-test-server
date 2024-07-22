import requests
from bs4 import BeautifulSoup
import re
import sqlite3
from typing import List, Dict, Optional, Tuple
import hashlib
import os
from database import insert_product

def get_product_title(product_soup: BeautifulSoup) -> str:
    """
    Extracts the product title from the HTML soup.

    Args:
        product_soup (BeautifulSoup): The BeautifulSoup object containing product HTML.

    Returns:
        str: The product title.
    """
    try:
        title_html = product_soup.find(attrs={"class": re.compile('.product.*(title|brand|name)')})
        return title_html.text.strip() if title_html else ''
    except Exception as e:
        print(f"An error occurred while extracting the product title: {e}")
        return ''

def get_product_price(product_soup: BeautifulSoup) -> str:
    """
    Extracts the product price from the HTML soup.

    Args:
        product_soup (BeautifulSoup): The BeautifulSoup object containing product HTML.

    Returns:
        str: The product price.
    """
    try:
        del_tags = product_soup.find_all('del')
        for del_tag in del_tags:
            del_tag.decompose()

        price_html = product_soup.find("span", attrs={"class": re.compile('.*price.*', flags=re.I)})
        return price_html.text.strip() if price_html else ''
    except Exception as e:
        print(f"An error occurred while extracting the product price: {e}")
        return ''

def get_image_url(product_soup: BeautifulSoup) -> str:
    """
    Extracts the product image URL from the HTML soup.

    Args:
        product_soup (BeautifulSoup): The BeautifulSoup object containing product HTML.

    Returns:
        str: The product image URL.
    """
    try:
        images = product_soup.findAll("img")
        for image in images:
            if image.get('src').startswith('http'):
                return image.get('src')
        return ''
    except Exception as e:
        print(f"An error occurred while extracting the product image URL: {e}")
        return ''

def scrape_catalogue(db_name: str, url: str, num_pages: int, proxy_string: Optional[str] = None) -> Tuple[List[Dict[str, str]], int, int]:
    """
    Scrapes product information from a catalogue and stores it in a SQLite database.
    Returns the list of products and the counts of inserted and existing products.

    Args:
        url (str): The base URL of the catalogue.
        num_pages (int): The number of pages to scrape.
        db_name (str): The name of the SQLite database file.
        proxy_string (Optional[str]): The proxy string for making requests.

    Returns:
        Tuple[List[Dict[str, str]], int, int]: A list of dictionaries containing product information,
        the count of newly inserted products, and the count of already existing products.
    """
    proxies = {
        'http': proxy_string,
        'https': proxy_string
    } if proxy_string else None
    
    product_info = []
    inserted_count = 0
    existing_count = 0

    for page in range(1, num_pages + 1):
        page_url = f"{url}/page/{page}"
        try:
            response = requests.get(page_url, proxies=proxies)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            products_html_content = soup.findAll("div", {"class" : re.compile('.*product.*(card|details|inner).*')})

            for product_html in products_html_content:
                product_soup = BeautifulSoup(str(product_html), 'html.parser')
                
                product_title = get_product_title(product_soup)
                product_price = get_product_price(product_soup)
                product_image_url = get_image_url(product_soup)

                product_info.append({
                    'product_title': product_title,
                    'product_price': product_price,
                    'product_image_url': product_image_url,
                })
                
                # Insert product into SQLite database and update counts
                if insert_product(db_name, product_title, product_price, product_image_url):
                    inserted_count += 1
                else:
                    existing_count += 1
        except requests.RequestException as e:
            print(f"An error occurred while making a request to {page_url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing the page: {e}")
    
    return product_info, inserted_count, existing_count


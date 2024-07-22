import requests
from bs4 import BeautifulSoup
import re
from typing import List, Dict, Optional
from fastapi import HTTPException

def get_product_title(product_soup: BeautifulSoup) -> str:
    """
    Extracts the product title from the HTML soup.

    Args:
        product_soup (BeautifulSoup): The BeautifulSoup object containing product HTML.

    Returns:
        str: The product title.
    """
    try:
        title_html = product_soup.find(attrs={"class": re.compile('.*product.*(title|brand|name)')})
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

        price_html = product_soup.find("span", attrs={"class": re.compile('.*(price|cost).*', flags=re.I)})
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

def check_url_accessibility(url: str) -> None:
    """
    Checks if the provided URL is accessible.

    Args:
        url (str): The URL to check.

    Raises:
        HTTPException: If the URL is not accessible.
    """
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="URL is not accessible")
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to access URL: {e}")


def scrape_catalogue(url: str, num_pages: int, proxy_string: Optional[str] = None) -> List[Dict[str, str]]:
    """
    Scrapes product information from a catalogue and stores it in a SQLite database.
    Returns the list of products and the counts of inserted and existing products.

    Args:
        url (str): The base URL of the catalogue.
        num_pages (int): The number of pages to scrape.
        db_name (str): The name of the SQLite database file.
        proxy_string (Optional[str]): The proxy string for making requests.

    Returns:
        List[Dict[str, str]]: A list of dictionaries containing product information.
    """
    
    check_url_accessibility(url)
    
    proxies = {
        'http': proxy_string,
        'https': proxy_string
    } if proxy_string else None
    
    product_info = []
    
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
                
        except requests.RequestException as e:
            print(f"An error occurred while making a request to {page_url}: {e}")
        except Exception as e:
            print(f"An unexpected error occurred while processing the page: {e}")
    
    return product_info


import requests
from bs4 import BeautifulSoup
import re

def get_product_title(product_soup):
    title_html = product_soup.find(attrs={"class": re.compile('.*product.*(title|brand|name)')})
    title = ''

    if title_html:
        title = title_html.text.strip()

    return title

def get_product_price(product_soup):
    del_tags = product_soup.find_all('del')
    for del_tag in del_tags:
        del_tag.decompose()

    price = ''
    price_html = product_soup.find("span", attrs={"class": re.compile('.*(price|cost).*', flags=re.I)})
    if price_html:
        price = price_html.text.strip()

    return price

def get_image_url(product_soup):
    images = product_soup.findAll("img")

    image_url = ''

    for image in images:
        if image.get('src').startswith('http'):
            image_url = image.get('src').strip()
            break
    
    return image_url


def scrape_catalogue(url, num_pages, proxy_string=None):
    proxies = {
        'http': proxy_string,
        'https': proxy_string
    } if proxy_string else None
    
    product_info = []

    for page in range(1, num_pages + 1):
        page_url = f"{url}/page/{page}"
        response = requests.get(page_url, proxies=proxies)
        soup = BeautifulSoup(response.content, 'html.parser')

        products_html_content = soup.findAll("div", {"class" : re.compile('.*product.*(card|details|inner).*')})

        print(f'Number of products for page {page}', len(products_html_content))
        for product_html in products_html_content:
            product_soup = BeautifulSoup(f"<html>{product_html}</html>", 'html.parser')
            
            product_title = get_product_title(product_soup)
            
            product_price = get_product_price(product_soup)
            
            product_image_url = get_image_url(product_soup)

            product_info.append({
                'product_title': product_title,
                'product_price': product_price,
                'product_image_url': product_image_url,
            })
    
    return product_info

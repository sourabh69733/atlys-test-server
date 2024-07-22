import unittest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
from scrape_catalogue import get_product_title, get_product_price, get_image_url, scrape_catalogue

class TestScrapeCatalogue(unittest.TestCase):

    def setUp(self):
        self.sample_html = """
        <div class="product-details">
            <span class="product-title">Sample Product</span>
            <span class="price">$19.99</span>
            <del>$29.99</del>
            <img src="http://example.com/sample.jpg" />
        </div>
        """
        self.sample_html_missing_title = """
        <div class="product-details">
            <span class="price">$19.99</span>
            <del>$29.99</del>
            <img src="http://example.com/sample.jpg" />
        </div>
        """
        self.sample_html_missing_price = """
        <div class="product-details">
            <span class="product-title">Sample Product</span>
            <img src="http://example.com/sample.jpg" />
        </div>
        """
        self.sample_html_missing_image = """
        <div class="product-details">
            <span class="product-title">Sample Product</span>
            <span class="price">$19.99</span>
            <del>$29.99</del>
        </div>
        """
        self.sample_html_different_structure = """
        <div class="product-card">
            <h2 class="product-name">Another Product</h2>
            <span class="cost">$9.99</span>
            <del>$19.99</del>
            <img src="http://example.com/another.jpg" />
        </div>
        """

        self.soup = BeautifulSoup(self.sample_html, 'html.parser')
        self.soup_missing_title = BeautifulSoup(self.sample_html_missing_title, 'html.parser')
        self.soup_missing_price = BeautifulSoup(self.sample_html_missing_price, 'html.parser')
        self.soup_missing_image = BeautifulSoup(self.sample_html_missing_image, 'html.parser')
        self.soup_different_structure = BeautifulSoup(self.sample_html_different_structure, 'html.parser')

    def test_get_product_title(self):
        title = get_product_title(self.soup)
        self.assertEqual(title, "Sample Product")

    def test_get_product_title_missing(self):
        title = get_product_title(self.soup_missing_title)
        self.assertEqual(title, "")

    def test_get_product_price(self):
        price = get_product_price(self.soup)
        self.assertEqual(price, "$19.99")

    def test_get_product_price_missing(self):
        price = get_product_price(self.soup_missing_price)
        self.assertEqual(price, "")

    def test_get_image_url(self):
        image_url = get_image_url(self.soup)
        self.assertEqual(image_url, "http://example.com/sample.jpg")

    def test_get_image_url_missing(self):
        image_url = get_image_url(self.soup_missing_image)
        self.assertEqual(image_url, "")

    def test_get_product_title_different_structure(self):
        title = get_product_title(self.soup_different_structure)
        self.assertEqual(title, "Another Product")

    def test_get_product_price_different_structure(self):
        price = get_product_price(self.soup_different_structure)
        self.assertEqual(price, "$9.99")

    def test_get_image_url_different_structure(self):
        image_url = get_image_url(self.soup_different_structure)
        self.assertEqual(image_url, "http://example.com/another.jpg")

    @patch('requests.get')
    def test_scrape_catalogue(self, mock_get):
        # Mock the HTML content of the page
        mock_response = Mock()
        mock_response.content = f"<html>{self.sample_html}</html>"
        mock_get.return_value = mock_response

        # Test scraping function
        url = "http://example.com/shop"
        num_pages = 1
        products = scrape_catalogue(url, num_pages)

        expected_products = [{
            'product_title': 'Sample Product',
            'product_price': '$19.99',
            'product_image_url': 'http://example.com/sample.jpg',
        }]

        self.assertEqual(products, expected_products)

if __name__ == '__main__':
    unittest.main()

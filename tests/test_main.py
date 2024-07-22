import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_scrape_catalogue_success():
    # Mock data for a successful scrape
    url = "https://dentalstall.com/shop"
    num_pages = 1
    
    # Simulate a successful scrape by calling the real endpoint
    response = client.post("/scrape", params={"url": url, "num_pages": num_pages})
    
    assert response.status_code == 200
    json_response = response.json()
    
    print('response', json_response)
    
    assert json_response["status"] == "ok"
    assert "inserted_count" in json_response
    assert "existing_count" in json_response
    assert "total_products" in json_response
    
# def test_scrape_catalogue_failure():
#     # To test failure, you need to ensure the conditions lead to a failure scenario
#     # For this example, we'll use a URL that doesn't exist or a bad request
#     url = "https://invalid-url.com"
#     num_pages = 1

#     # Simulate a failure by calling the real endpoint
#     response = client.post("/scrape", params={"url": url, "num_pages": num_pages})
    
#     assert response.status_code == 500
#     json_response = response.json()
#     assert "detail" in json_response

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

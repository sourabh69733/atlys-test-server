# FastAPI Server Setup and Usage

## Overview

This project sets up a FastAPI server for handling product data scraping and management. The server is designed to be run in a production environment using `uvicorn` as the ASGI server.

### Project Structure
```
/project-root
│
├── main.py # Main FastAPI application file
├── requirements.txt # List of Python dependencies
├── setup.sh # Setup script for creating environment and running server
├── /tests # Directory containing unit tests
│ └── test_main.py # Unit tests for the FastAPI application
└── /venv # Python virtual environment directory (auto-created)

```
### Main Components

1. **`main.py`**:
   - Contains the FastAPI application with endpoints to manage product scraping.
   - `GET /`: Returns a basic "Hello World" message.
   - `POST /scrape`: Triggers the product scraping process and stores data in the database.

2. **`requirements.txt`**:
   - Lists the dependencies required for the project:
     - `fastapi`: Web framework for building APIs.
     - `uvicorn`: ASGI server to serve FastAPI.
     - `requests`: For making HTTP requests.
     - `beautifulsoup4`: For parsing HTML content.
     - `pytest`: Testing framework for unit tests.

3. **`setup.sh`**:
   - A script to set up the Python virtual environment, install dependencies, and start the FastAPI server.
   - Supports macOS, Linux, and Windows environments.

4. **`/tests`**:
   - Contains unit tests for verifying the functionality of the FastAPI application.
   - `test_main.py`: Test cases for the `/scrape` endpoint and other functionalities.

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://your-repository-url.git
cd your-project-directory
```

### 2. Run the Setup Script
On macOS/Linux:
Make the script executable and run it:
```bash
chmod +x setup.sh
./setup.sh
```
On Windows:
Open PowerShell and run:

```
.\setup.sh
```

### 3. Verify the Setup
The FastAPI server should start and be accessible at `http://0.0.0.0:8000`.

Check the interactive API documentation at `http://0.0.0.0:8000/docs`.

### 4. Test APIs
Send post request to endpoint `http://0.0.0.0:8000/scrape` with `url` and `num_pages` params.

Sample Request
```
curl -X 'POST' \
  'http://0.0.0.0:8000/scrape?url=https%3A%2F%2Fdentalstall.com%2Fshop&num_pages=2' \
  -H 'accept: application/json' \
  -d ''
```

Sample Response will be 
```
{
  "status": "ok",
  "inserted_count": 48,
  "existing_count": 96,
  "total_products": 144
}
```



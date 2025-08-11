"""
Test script to demonstrate API functionality.
This script shows how to test your API endpoints manually.

For production testing, you would use tools like:
- Postman (GUI tool)
- curl (command line)
- Python requests library
- Django's test framework
"""

import requests
import json

# Base URL for your API
BASE_URL = "http://localhost:8000/api"

def test_book_list():
    """Test getting list of all books"""
    print("\n=== Testing Book List (GET /api/books/) ===")
    response = requests.get(f"{BASE_URL}/books/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")

def test_book_create():
    """Test creating a new book"""
    print("\n=== Testing Book Create (POST /api/books/create/) ===")
    
    # First create an author
    author_data = {"name": "Test Author"}
    author_response = requests.post("http://localhost:8000/admin/", json=author_data)
    
    # Then create a book
    book_data = {
        "title": "Test Book",
        "publication_year": 2023,
        "author": 1  # Assuming author ID 1 exists
    }
    
    response = requests.post(f"{BASE_URL}/books/create/", json=book_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

def test_book_detail():
    """Test getting a specific book"""
    print("\n=== Testing Book Detail (GET /api/books/1/) ===")
    response = requests.get(f"{BASE_URL}/books/1/")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print(f"Response: {response.json()}")
    else:
        print(f"Response: {response.text}")

if __name__ == "__main__":
    print("Testing API Endpoints...")
    print("Make sure your Django server is running on http://localhost:8000")
    
    try:
        test_book_list()
        test_book_detail()
        test_book_create()
    except requests.ConnectionError:
        print("\n❌ Error: Could not connect to server.")
        print("Make sure Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {e}")

"""
Comprehensive API Testing Script for Filtering, Searching, and Ordering

This script demonstrates how to use the advanced query capabilities:
- Filtering: Narrow down results by specific criteria
- Searching: Find books by text search across multiple fields  
- Ordering: Sort results by different fields

Before running this script:
1. Make sure Django server is running: python manage.py runserver
2. Create some test data in Django admin or shell
"""

import requests
import json

BASE_URL = "http://localhost:8000/api"

def print_response(title, response):
    """Helper function to print formatted response"""
    print(f"\n{'='*60}")
    print(f"🧪 {title}")
    print(f"{'='*60}")
    print(f"📍 URL: {response.url}")
    print(f"📊 Status Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"📈 Results Count: {len(data)}")
        
        if data:
            print(f"📚 Sample Results:")
            for i, book in enumerate(data[:3]):  # Show first 3 results
                print(f"   {i+1}. '{book['title']}' by Author ID {book['author']} ({book['publication_year']})")
            if len(data) > 3:
                print(f"   ... and {len(data) - 3} more")
    else:
        print(f"❌ Error: {response.text}")

def test_basic_list():
    """Test basic book listing without any parameters"""
    response = requests.get(f"{BASE_URL}/books/")
    print_response("Basic Book List (No Parameters)", response)

def test_filtering():
    """Test various filtering options"""
    
    # Filter by title containing text
    response = requests.get(f"{BASE_URL}/books/?title__icontains=harry")
    print_response("FILTER: Books with 'harry' in title", response)
    
    # Filter by publication year
    response = requests.get(f"{BASE_URL}/books/?publication_year__gte=2000")
    print_response("FILTER: Books published 2000 or later", response)
    
    # Filter by publication year range
    response = requests.get(f"{BASE_URL}/books/?publication_year__range=1990,2010")
    print_response("FILTER: Books published between 1990-2010", response)
    
    # Filter by author name
    response = requests.get(f"{BASE_URL}/books/?author_name__icontains=rowling")
    print_response("FILTER: Books by authors with 'rowling' in name", response)

def test_searching():
    """Test search functionality"""
    
    # Search for "harry" across title and author name
    response = requests.get(f"{BASE_URL}/books/?search=harry")
    print_response("SEARCH: 'harry' in title or author name", response)
    
    # Search for "django"
    response = requests.get(f"{BASE_URL}/books/?search=django")
    print_response("SEARCH: 'django' in title or author name", response)
    
    # Search with multiple words
    response = requests.get(f"{BASE_URL}/books/?search=animal farm")
    print_response("SEARCH: 'animal farm' in title or author name", response)

def test_ordering():
    """Test ordering/sorting functionality"""
    
    # Order by title A-Z
    response = requests.get(f"{BASE_URL}/books/?ordering=title")
    print_response("ORDER: By title (A-Z)", response)
    
    # Order by title Z-A
    response = requests.get(f"{BASE_URL}/books/?ordering=-title")
    print_response("ORDER: By title (Z-A)", response)
    
    # Order by publication year (oldest first)
    response = requests.get(f"{BASE_URL}/books/?ordering=publication_year")
    print_response("ORDER: By publication year (oldest first)", response)
    
    # Order by publication year (newest first)
    response = requests.get(f"{BASE_URL}/books/?ordering=-publication_year")
    print_response("ORDER: By publication year (newest first)", response)

def test_combined_queries():
    """Test combining filtering, searching, and ordering"""
    
    # Search + Order
    response = requests.get(f"{BASE_URL}/books/?search=book&ordering=-publication_year")
    print_response("COMBINED: Search 'book' + Order by year (newest first)", response)
    
    # Filter + Order
    response = requests.get(f"{BASE_URL}/books/?publication_year__gte=1900&ordering=title")
    print_response("COMBINED: Filter (year ≥ 1900) + Order by title", response)
    
    # Search + Filter + Order
    response = requests.get(f"{BASE_URL}/books/?search=a&publication_year__gte=1990&ordering=-publication_year")
    print_response("COMBINED: Search 'a' + Filter (year ≥ 1990) + Order by year (newest)", response)

def test_list_create_endpoint():
    """Test the combined list/create endpoint with same capabilities"""
    
    response = requests.get(f"{BASE_URL}/books/list-create/?search=book&ordering=title")
    print_response("LIST-CREATE ENDPOINT: Search + Order", response)

def show_usage_examples():
    """Show practical usage examples"""
    print(f"\n{'='*60}")
    print("📖 PRACTICAL USAGE EXAMPLES")
    print(f"{'='*60}")
    
    examples = [
        ("Find books with 'Python' in title", "?title__icontains=python"),
        ("Find recent books (2020 or later)", "?publication_year__gte=2020"),
        ("Find books from the 2000s", "?publication_year__range=2000,2009"),
        ("Search for 'Django' anywhere", "?search=django"),
        ("Get books sorted by newest first", "?ordering=-publication_year"),
        ("Find 'Harry Potter' books by newest", "?search=harry potter&ordering=-publication_year"),
        ("Find recent Python books", "?title__icontains=python&publication_year__gte=2020"),
    ]
    
    for description, params in examples:
        print(f"\n🔍 {description}:")
        print(f"   GET {BASE_URL}/books/{params}")

def main():
    """Main test function"""
    print("🚀 Starting API Query Capabilities Test")
    print("Make sure your Django server is running on http://localhost:8000")
    print("And that you have some test data in your database!")
    
    try:
        # Basic functionality
        test_basic_list()
        
        # Individual features
        test_filtering()
        test_searching() 
        test_ordering()
        
        # Combined features
        test_combined_queries()
        
        # Alternative endpoint
        test_list_create_endpoint()
        
        # Usage examples
        show_usage_examples()
        
        print(f"\n{'='*60}")
        print("✅ All tests completed! Check the results above.")
        print("📝 Try these URLs in your browser or Postman for interactive testing.")
        
    except requests.ConnectionError:
        print("\n❌ Error: Could not connect to server.")
        print("Make sure Django server is running: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()

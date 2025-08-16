"""
Simple demonstration of filtering, searching, and ordering capabilities.

This script shows practical examples of how to use the new API features.
Run this after starting your Django server.
"""

def demonstrate_features():
    """Show examples of the new API capabilities"""
    
    print("🚀 Django REST Framework Advanced Query Features")
    print("=" * 60)
    
    base_url = "http://127.0.0.1:8000/api/books/"
    
    examples = [
        {
            "title": "📚 Basic List (All Books)",
            "url": base_url,
            "description": "Get all books with default ordering (by title)"
        },
        {
            "title": "🔍 Filter by Publication Year",
            "url": base_url + "?publication_year__gte=2000",
            "description": "Show only books published in 2000 or later"
        },
        {
            "title": "🔎 Search for 'Harry'",
            "url": base_url + "?search=harry",
            "description": "Search for 'harry' in book title or author name"
        },
        {
            "title": "📊 Order by Newest First",
            "url": base_url + "?ordering=-publication_year",
            "description": "Sort books by publication year (newest first)"
        },
        {
            "title": "🎯 Combined Query",
            "url": base_url + "?search=book&ordering=title&publication_year__gte=1990",
            "description": "Search 'book' + filter year ≥ 1990 + sort by title"
        },
        {
            "title": "📖 Filter by Author Name",
            "url": base_url + "?author_name__icontains=austen",
            "description": "Find books by authors with 'austen' in their name"
        }
    ]
    
    print("\n🧪 Try these URLs in your browser:")
    print("-" * 60)
    
    for i, example in enumerate(examples, 1):
        print(f"\n{i}. {example['title']}")
        print(f"   📍 URL: {example['url']}")
        print(f"   📝 What it does: {example['description']}")
    
    print(f"\n{'=' * 60}")
    print("💡 Tips for testing:")
    print("• Copy any URL above into your browser")
    print("• Use Django REST Framework's browsable API interface")
    print("• Try modifying the parameters to see different results")
    print("• Combine multiple parameters with &")
    
    print(f"\n🔧 Parameter Examples:")
    print("• ?search=text                    (search in title and author)")
    print("• ?title__icontains=python        (books with 'python' in title)")
    print("• ?publication_year=2020          (exact year match)")
    print("• ?publication_year__gte=2000     (year 2000 or later)")
    print("• ?publication_year__range=2000,2010  (between years)")
    print("• ?ordering=title                 (sort A-Z)")
    print("• ?ordering=-title                (sort Z-A)")
    print("• ?author_name__icontains=smith   (author name contains 'smith')")

if __name__ == "__main__":
    demonstrate_features()

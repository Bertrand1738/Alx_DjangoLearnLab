#!/usr/bin/env python
"""
Test script to verify our relationship_app models and queries work correctly.
Run this with: python manage.py shell < test_queries.py
"""

# Import our models and query functions
from relationship_app.models import Author, Book, Library, Librarian
from relationship_app.query_samples import *

print("🧪 Testing Django Models and Relationships")
print("=" * 50)

# Test 1: Create sample data
print("\n1️⃣ Creating sample data...")
try:
    # Clear existing data to avoid conflicts
    Author.objects.all().delete()
    Book.objects.all().delete()
    Library.objects.all().delete()
    Librarian.objects.all().delete()
    
    # Create fresh sample data
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George Orwell")
    print(f"✅ Created authors: {author1.name}, {author2.name}")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    book3 = Book.objects.create(title="1984", author=author2)
    print(f"✅ Created {Book.objects.count()} books")
    
    # Create library
    library = Library.objects.create(name="Central Library")
    library.books.add(book1, book2, book3)
    print(f"✅ Created library: {library.name} with {library.books.count()} books")
    
    # Create librarian
    librarian = Librarian.objects.create(name="Alice Smith", library=library)
    print(f"✅ Created librarian: {librarian.name}")
    
except Exception as e:
    print(f"❌ Error creating sample data: {e}")

# Test 2: Query books by author (ForeignKey relationship)
print("\n2️⃣ Testing ForeignKey relationship - Books by Author:")
try:
    books = query_all_books_by_author("J.K. Rowling")
    print(f"✅ Found {books.count()} books by J.K. Rowling")
except Exception as e:
    print(f"❌ Error querying books by author: {e}")

# Test 3: List books in library (ManyToMany relationship)
print("\n3️⃣ Testing ManyToMany relationship - Books in Library:")
try:
    books = list_all_books_in_library("Central Library")
    print(f"✅ Found {books.count()} books in Central Library")
except Exception as e:
    print(f"❌ Error listing books in library: {e}")

# Test 4: Retrieve librarian (OneToOne relationship)
print("\n4️⃣ Testing OneToOne relationship - Librarian for Library:")
try:
    librarian = retrieve_librarian_for_library("Central Library")
    if librarian:
        print(f"✅ Found librarian: {librarian.name}")
    else:
        print("❌ No librarian found")
except Exception as e:
    print(f"❌ Error retrieving librarian: {e}")

print("\n🎉 All tests completed!")

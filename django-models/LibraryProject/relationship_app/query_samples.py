"""
Django ORM Query Samples for Relationship App

This file contains sample queries demonstrating relationships between models.
To use these functions, run them in Django shell:

1. Open Django shell: python manage.py shell
2. Import this file: from relationship_app.query_samples import *
3. Run the functions: query_all_books_by_author("Author Name")

Note: Make sure you have sample data in your database first.
"""

# Import our models
from .models import Author, Book, Library, Librarian


def query_all_books_by_author(author_name):
    """
    Query all books by a specific author.
    
    This demonstrates a ForeignKey relationship query.
    When a Book has a ForeignKey to Author, we can:
    1. Filter books by author using the author field
    2. Use double underscores (__) to access related fields
    
    Args:
        author_name (str): Name of the author to search for
    
    Returns:
        QuerySet: All books by the specified author
    """
    try:
        # Method 1: Get the author first, then get their books
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        
        print(f"Books by {author_name}:")
        for book in books:
            print(f"  - {book.title}")
        
        return books
        
    except Author.DoesNotExist:
        print(f"Author '{author_name}' not found.")
        return Book.objects.none()  # Return empty QuerySet


def query_all_books_by_author_alternative(author_name):
    """
    Alternative way to query books by author using field lookups.
    
    This shows how to use the double underscore notation to access
    related model fields directly in the query.
    """
    # Method 2: Use field lookup with double underscores
    books = Book.objects.filter(author__name=author_name)
    
    print(f"Books by {author_name} (alternative method):")
    for book in books:
        print(f"  - {book.title} by {book.author.name}")
    
    return books


def list_all_books_in_library(library_name):
    """
    List all books in a library.
    
    This demonstrates a ManyToMany relationship query.
    When Library has a ManyToManyField to Book, we can:
    1. Access the related books using the field name
    2. Use .all() to get all related objects
    
    Args:
        library_name (str): Name of the library
    
    Returns:
        QuerySet: All books in the specified library
    """
    try:
        # Get the library first
        library = Library.objects.get(name=library_name)
        
        # Access all books in the library using the ManyToMany field
        books = library.books.all()
        
        print(f"Books in {library_name}:")
        if books.exists():
            for book in books:
                print(f"  - {book.title} by {book.author.name}")
        else:
            print("  No books found in this library.")
        
        return books
        
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return Book.objects.none()


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    
    This demonstrates a OneToOne relationship query.
    When Librarian has a OneToOneField to Library, we can:
    1. Access the librarian from the library using reverse lookup
    2. Use try/except to handle cases where no librarian exists
    
    Args:
        library_name (str): Name of the library
    
    Returns:
        Librarian or None: The librarian for the specified library
    """
    try:
        # Get the library first
        library = Library.objects.get(name=library_name)
        
        # Access the librarian using reverse OneToOne relationship
        # Django automatically creates a reverse relationship
        librarian = library.librarian  # This uses the reverse lookup
        
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
        
    except Library.DoesNotExist:
        print(f"Library '{library_name}' not found.")
        return None
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library_name}.")
        return None


def retrieve_librarian_alternative(library_name):
    """
    Alternative way to retrieve librarian using direct query.
    
    This shows another approach using the Librarian model directly.
    """
    try:
        # Query the Librarian model directly using library field lookup
        librarian = Librarian.objects.get(library__name=library_name)
        
        print(f"Librarian for {library_name}: {librarian.name}")
        return librarian
        
    except Librarian.DoesNotExist:
        print(f"No librarian found for library '{library_name}'.")
        return None


def demonstrate_all_queries():
    """
    Demonstrate all query types with sample data.
    
    This function shows how to use all the query functions above.
    Note: This assumes you have sample data in your database.
    """
    print("=" * 50)
    print("DJANGO ORM QUERY DEMONSTRATIONS")
    print("=" * 50)
    
    # You would need to create sample data first
    # For example, using Django shell or admin interface
    
    print("\n1. Querying books by author:")
    print("-" * 30)
    # Example: query_all_books_by_author("J.K. Rowling")
    print("Usage: query_all_books_by_author('Author Name')")
    
    print("\n2. Listing books in a library:")
    print("-" * 30)
    # Example: list_all_books_in_library("Central Library")
    print("Usage: list_all_books_in_library('Library Name')")
    
    print("\n3. Retrieving librarian for a library:")
    print("-" * 30)
    # Example: retrieve_librarian_for_library("Central Library")
    print("Usage: retrieve_librarian_for_library('Library Name')")
    
    print("\nTo run these queries with actual data:")
    print("1. Create some sample data using Django admin or shell")
    print("2. Uncomment the example calls above")
    print("3. Run this script: python query_samples.py")


# Additional helper functions for creating sample data
def create_sample_data():
    """
    Create sample data for testing our queries.
    
    This function demonstrates how to create model instances
    and establish relationships between them.
    """
    print("Creating sample data...")
    
    # Create authors
    author1, created = Author.objects.get_or_create(name="J.K. Rowling")
    author2, created = Author.objects.get_or_create(name="George Orwell")
    
    # Create books
    book1, created = Book.objects.get_or_create(
        title="Harry Potter and the Philosopher's Stone",
        author=author1
    )
    book2, created = Book.objects.get_or_create(
        title="Harry Potter and the Chamber of Secrets",
        author=author1
    )
    book3, created = Book.objects.get_or_create(
        title="1984",
        author=author2
    )
    
    # Create library
    library, created = Library.objects.get_or_create(name="Central Library")
    
    # Add books to library (ManyToMany relationship)
    library.books.add(book1, book2, book3)
    
    # Create librarian
    librarian, created = Librarian.objects.get_or_create(
        name="Alice Smith",
        library=library
    )
    
    print("Sample data created successfully!")
    return author1, author2, book1, book2, book3, library, librarian
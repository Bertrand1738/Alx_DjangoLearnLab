"""
Django ORM Query Samples - Simplified Version

This file contains the same queries but structured to work better with Django shell.
Run this using: python manage.py shell < relationship_app/django_queries.py

Or copy and paste the functions into Django shell manually.
"""

# Import our models
from relationship_app.models import Author, Book, Library, Librarian

def query_all_books_by_author(author_name):
    """
    Query all books by a specific author.
    
    BEGINNER EXPLANATION:
    - This function shows how to find all books written by a specific author
    - We use Django's ORM (Object-Relational Mapping) to query the database
    - The relationship between Book and Author is a ForeignKey (many books can have one author)
    
    Step by step:
    1. Find the author by name using Author.objects.get()
    2. Find all books by this author using Book.objects.filter()
    3. Display the results
    
    Args:
        author_name (str): The name of the author to search for
    """
    try:
        # Step 1: Find the author
        print(f"🔍 Looking for author: {author_name}")
        author = Author.objects.get(name=author_name)
        print(f"✅ Found author: {author.name}")
        
        # Step 2: Find all books by this author
        print(f"📚 Searching for books by {author.name}...")
        books = Book.objects.filter(author=author)
        
        # Step 3: Display results
        print(f"📖 Books by {author_name}:")
        if books.exists():
            for i, book in enumerate(books, 1):
                print(f"   {i}. {book.title}")
        else:
            print("   No books found for this author.")
        
        return books
        
    except Author.DoesNotExist:
        print(f"❌ Author '{author_name}' not found in the database.")
        print("💡 Tip: Make sure you've created this author first!")
        return Book.objects.none()


def list_all_books_in_library(library_name):
    """
    List all books in a library.
    
    BEGINNER EXPLANATION:
    - This function shows how to find all books in a specific library
    - The relationship between Library and Book is ManyToMany (many books can be in many libraries)
    - We access related objects using the field name (books) followed by .all()
    
    Step by step:
    1. Find the library by name
    2. Get all books in this library using the ManyToMany relationship
    3. Display the results with author information
    
    Args:
        library_name (str): The name of the library
    """
    try:
        # Step 1: Find the library
        print(f"🏛️  Looking for library: {library_name}")
        library = Library.objects.get(name=library_name)
        print(f"✅ Found library: {library.name}")
        
        # Step 2: Get all books in this library
        print(f"📚 Getting all books in {library.name}...")
        books = library.books.all()  # This uses the ManyToMany relationship
        
        # Step 3: Display results
        print(f"📖 Books in {library_name}:")
        if books.exists():
            for i, book in enumerate(books, 1):
                print(f"   {i}. '{book.title}' by {book.author.name}")
        else:
            print("   📭 No books found in this library.")
        
        print(f"📊 Total books: {books.count()}")
        return books
        
    except Library.DoesNotExist:
        print(f"❌ Library '{library_name}' not found in the database.")
        print("💡 Tip: Make sure you've created this library first!")
        return Book.objects.none()


def retrieve_librarian_for_library(library_name):
    """
    Retrieve the librarian for a library.
    
    BEGINNER EXPLANATION:
    - This function shows how to find the librarian assigned to a library
    - The relationship between Librarian and Library is OneToOne (one librarian per library)
    - We use reverse lookup to find the librarian from the library
    
    Step by step:
    1. Find the library by name
    2. Get the librarian using the OneToOne reverse relationship
    3. Display the result
    
    Args:
        library_name (str): The name of the library
    """
    try:
        # Step 1: Find the library
        print(f"🏛️  Looking for library: {library_name}")
        library = Library.objects.get(name=library_name)
        print(f"✅ Found library: {library.name}")
        
        # Step 2: Get the librarian using reverse OneToOne relationship
        print(f"👤 Looking for librarian of {library.name}...")
        librarian = library.librarian  # This uses the reverse OneToOne relationship
        
        # Step 3: Display result
        print(f"👨‍💼 Librarian for {library_name}: {librarian.name}")
        return librarian
        
    except Library.DoesNotExist:
        print(f"❌ Library '{library_name}' not found in the database.")
        print("💡 Tip: Make sure you've created this library first!")
        return None
    except Librarian.DoesNotExist:
        print(f"❌ No librarian assigned to {library_name}.")
        print("💡 Tip: You need to create a librarian and assign them to this library!")
        return None


def create_sample_data():
    """
    Create sample data for testing our queries.
    
    BEGINNER EXPLANATION:
    - This function creates test data so we can try our queries
    - It shows how to create objects and establish relationships
    - We use get_or_create() to avoid creating duplicates
    
    Step by step:
    1. Create authors
    2. Create books and link them to authors (ForeignKey)
    3. Create a library
    4. Add books to the library (ManyToMany)
    5. Create a librarian and assign them to the library (OneToOne)
    """
    print("🏗️  Creating sample data...")
    
    # Step 1: Create authors
    print("👨‍💻 Creating authors...")
    author1, created = Author.objects.get_or_create(name="J.K. Rowling")
    if created:
        print("   ✅ Created: J.K. Rowling")
    else:
        print("   ♻️  Already exists: J.K. Rowling")
        
    author2, created = Author.objects.get_or_create(name="George Orwell")
    if created:
        print("   ✅ Created: George Orwell")
    else:
        print("   ♻️  Already exists: George Orwell")
    
    # Step 2: Create books
    print("📚 Creating books...")
    book1, created = Book.objects.get_or_create(
        title="Harry Potter and the Philosopher's Stone",
        author=author1
    )
    if created:
        print("   ✅ Created: Harry Potter and the Philosopher's Stone")
    else:
        print("   ♻️  Already exists: Harry Potter and the Philosopher's Stone")
        
    book2, created = Book.objects.get_or_create(
        title="Harry Potter and the Chamber of Secrets",
        author=author1
    )
    if created:
        print("   ✅ Created: Harry Potter and the Chamber of Secrets")
    else:
        print("   ♻️  Already exists: Harry Potter and the Chamber of Secrets")
        
    book3, created = Book.objects.get_or_create(
        title="1984",
        author=author2
    )
    if created:
        print("   ✅ Created: 1984")
    else:
        print("   ♻️  Already exists: 1984")
    
    # Step 3: Create library
    print("🏛️  Creating library...")
    library, created = Library.objects.get_or_create(name="Central Library")
    if created:
        print("   ✅ Created: Central Library")
    else:
        print("   ♻️  Already exists: Central Library")
    
    # Step 4: Add books to library (ManyToMany relationship)
    print("📖 Adding books to library...")
    library.books.add(book1, book2, book3)
    print("   ✅ Added all books to Central Library")
    
    # Step 5: Create librarian
    print("👨‍💼 Creating librarian...")
    librarian, created = Librarian.objects.get_or_create(
        name="Alice Smith",
        library=library
    )
    if created:
        print("   ✅ Created: Alice Smith as librarian of Central Library")
    else:
        print("   ♻️  Already exists: Alice Smith")
    
    print("🎉 Sample data creation completed!")
    print("\n📊 Summary:")
    print(f"   - Authors: {Author.objects.count()}")
    print(f"   - Books: {Book.objects.count()}")
    print(f"   - Libraries: {Library.objects.count()}")
    print(f"   - Librarians: {Librarian.objects.count()}")


def run_all_demonstrations():
    """
    Run all query demonstrations with sample data.
    
    This function will:
    1. Create sample data if it doesn't exist
    2. Run all our query functions
    3. Show you how the relationships work
    """
    print("🚀 Starting Django ORM Query Demonstrations")
    print("=" * 60)
    
    # Create sample data first
    create_sample_data()
    
    print("\n" + "=" * 60)
    print("🔍 RUNNING QUERY DEMONSTRATIONS")
    print("=" * 60)
    
    # Demonstration 1: Query books by author
    print("\n1️⃣  DEMONSTRATION: Query all books by a specific author")
    print("-" * 50)
    query_all_books_by_author("J.K. Rowling")
    
    print("\n" + "-" * 50)
    query_all_books_by_author("George Orwell")
    
    # Demonstration 2: List books in library
    print("\n\n2️⃣  DEMONSTRATION: List all books in a library")
    print("-" * 50)
    list_all_books_in_library("Central Library")
    
    # Demonstration 3: Retrieve librarian
    print("\n\n3️⃣  DEMONSTRATION: Retrieve librarian for a library")
    print("-" * 50)
    retrieve_librarian_for_library("Central Library")
    
    print("\n" + "=" * 60)
    print("✅ All demonstrations completed!")
    print("=" * 60)


# Instructions for running this script
print("""
🎓 DJANGO ORM LEARNING GUIDE
============================

This script demonstrates Django ORM relationships:
- ForeignKey (Book → Author): Many books can have one author
- ManyToMany (Library ↔ Book): Many books can be in many libraries  
- OneToOne (Librarian → Library): One librarian per library

TO RUN THESE DEMONSTRATIONS:

Method 1: Django Shell (Recommended)
1. Run: python manage.py shell
2. Copy and paste: exec(open('relationship_app/django_queries.py').read())
3. Then run: run_all_demonstrations()

Method 2: Individual Functions
1. Run: python manage.py shell  
2. Copy and paste the functions you want to try
3. Call them individually like: query_all_books_by_author("J.K. Rowling")

Method 3: Interactive Testing
1. Run: python manage.py shell
2. Import: from relationship_app.django_queries import *
3. Run: create_sample_data()  # First time only
4. Try any function: query_all_books_by_author("J.K. Rowling")

Happy learning! 🚀
""")

# Simple test commands for Django shell
from relationship_app.models import Author, Book, Library, Librarian

# Test model creation
print("Testing model imports...")
print("Author model:", Author)
print("Book model:", Book)  
print("Library model:", Library)
print("Librarian model:", Librarian)

# Create a simple test
author = Author.objects.create(name="Test Author")
print(f"Created author: {author}")

book = Book.objects.create(title="Test Book", author=author)
print(f"Created book: {book}")

library = Library.objects.create(name="Test Library")
library.books.add(book)
print(f"Created library: {library}")

librarian = Librarian.objects.create(name="Test Librarian", library=library)
print(f"Created librarian: {librarian}")

print("✅ All models working correctly!")

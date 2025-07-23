# Script to create test data for authentication testing
# Run: python manage.py shell < create_auth_test_data.py

from relationship_app.models import Author, Book, Library, Librarian

print("Creating sample data for authentication testing...")

# Clear and create fresh data
Author.objects.all().delete()
Book.objects.all().delete()
Library.objects.all().delete()  
Librarian.objects.all().delete()

# Create authors
author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="George Orwell")

# Create books
book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
book2 = Book.objects.create(title="1984", author=author2)

# Create library
library = Library.objects.create(name="Central Library")
library.books.add(book1, book2)

# Create librarian
librarian = Librarian.objects.create(name="Alice Smith", library=library)

print("✅ Test data created!")
print("\nNow you can test:")
print("1. Register: http://localhost:8000/relationship_app/register/")
print("2. Login: http://localhost:8000/relationship_app/login/")
print("3. View books: http://localhost:8000/relationship_app/books/")
print("4. View library: http://localhost:8000/relationship_app/library/1/")
print("5. Logout: http://localhost:8000/relationship_app/logout/")

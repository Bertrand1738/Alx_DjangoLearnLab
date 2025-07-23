# Quick script to create test data for our views
# Run this in Django shell: python manage.py shell < create_test_data.py

from relationship_app.models import Author, Book, Library, Librarian

# Clear existing data
print("Clearing existing data...")
Author.objects.all().delete()
Book.objects.all().delete() 
Library.objects.all().delete()
Librarian.objects.all().delete()

# Create authors
print("Creating authors...")
author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="George Orwell")
author3 = Author.objects.create(name="Agatha Christie")

# Create books
print("Creating books...")
book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
book2 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
book3 = Book.objects.create(title="1984", author=author2)
book4 = Book.objects.create(title="Animal Farm", author=author2)
book5 = Book.objects.create(title="Murder on the Orient Express", author=author3)

# Create libraries
print("Creating libraries...")
library1 = Library.objects.create(name="Central Library")
library2 = Library.objects.create(name="University Library")

# Add books to libraries
print("Adding books to libraries...")
library1.books.add(book1, book2, book3)
library2.books.add(book3, book4, book5)

# Create librarians
print("Creating librarians...")
librarian1 = Librarian.objects.create(name="Alice Smith", library=library1)
librarian2 = Librarian.objects.create(name="Bob Johnson", library=library2)

print("✅ Test data created successfully!")
print(f"Authors: {Author.objects.count()}")
print(f"Books: {Book.objects.count()}")
print(f"Libraries: {Library.objects.count()}")
print(f"Librarians: {Librarian.objects.count()}")

print("\nNow you can visit:")
print("- http://localhost:8000/relationship_app/books/ (to see all books)")
print("- http://localhost:8000/relationship_app/library/1/ (to see Central Library)")
print("- http://localhost:8000/relationship_app/library/2/ (to see University Library)")

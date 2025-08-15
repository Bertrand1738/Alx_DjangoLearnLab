"""
Django shell commands to create test data.
Copy and paste these commands into Django shell (python manage.py shell)
"""

from api.models import Author, Book

# Create test authors
author1 = Author.objects.create(name="J.K. Rowling")
author2 = Author.objects.create(name="George Orwell")

# Create test books
book1 = Book.objects.create(
    title="Harry Potter and the Philosopher's Stone",
    publication_year=1997,
    author=author1
)

book2 = Book.objects.create(
    title="1984",
    publication_year=1949,
    author=author2
)

book3 = Book.objects.create(
    title="Animal Farm",
    publication_year=1945,
    author=author2
)

print("Test data created successfully!")
print(f"Authors: {Author.objects.count()}")
print(f"Books: {Book.objects.count()}")

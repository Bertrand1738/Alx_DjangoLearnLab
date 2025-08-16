"""
Author and Book models for advanced API project.

Author: Represents a book author with a name field.
Book: Represents a book with title, publication year, and a foreign key to Author.
The relationship is one-to-many: one Author can have many Books.
"""
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    # Author's name

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)
    # Book's title, publication year, and link to Author

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

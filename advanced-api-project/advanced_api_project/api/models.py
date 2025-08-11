from django.db import models
from datetime import datetime

class Author(models.Model):
    """
    Represents an author of one or more books.
    One Author -> Many Books (One-to-Many Relationship)
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book written by an Author.
    Each Book is linked to exactly one Author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name='books',  # Used in serializers for reverse lookup
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

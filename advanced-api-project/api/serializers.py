"""
Custom serializers for Author and Book models.

BookSerializer: Serializes all fields of Book and validates publication_year is not in the future.
AuthorSerializer: Serializes Author's name and includes nested BookSerializer for related books.
Handles one-to-many relationship: Author -> Books.
"""
from rest_framework import serializers
from .models import Author, Book
from datetime import datetime

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value

class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)
    # Nested serializer for related books

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

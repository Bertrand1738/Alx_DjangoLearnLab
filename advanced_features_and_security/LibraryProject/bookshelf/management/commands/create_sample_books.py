from django.core.management.base import BaseCommand
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Create sample books for testing permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('📚 Creating sample books...'))
        
        # Sample books data
        books_data = [
            {
                'title': 'Django for Beginners',
                'author': 'William S. Vincent',
                'publication_year': 2022
            },
            {
                'title': 'Python Crash Course',
                'author': 'Eric Matthes',
                'publication_year': 2019
            },
            {
                'title': 'Clean Code',
                'author': 'Robert C. Martin',
                'publication_year': 2008
            },
            {
                'title': 'The Pragmatic Programmer',
                'author': 'David Thomas',
                'publication_year': 1999
            }
        ]
        
        # Delete existing books
        Book.objects.all().delete()
        self.stdout.write('🗑️  Cleared existing books')
        
        # Create sample books
        for book_data in books_data:
            book = Book.objects.create(**book_data)
            self.stdout.write(f'✅ Created: {book.title} by {book.author} ({book.publication_year})')
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Created {len(books_data)} sample books!'))
        self.stdout.write('Now you can test permissions with real data.')

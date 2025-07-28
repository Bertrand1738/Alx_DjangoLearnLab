"""
Django Management Command for Query Demonstrations

This is the proper way to create custom Django commands.
Run this with: python manage.py run_queries

BEGINNER EXPLANATION:
- Django management commands are the proper way to run scripts that need Django environment
- They automatically handle the Django setup, so we don't need django.setup()
- Commands go in app/management/commands/ directory
- Each command is a Python file with a Command class
"""

from django.core.management.base import BaseCommand
from relationship_app.models import Author, Book, Library, Librarian


class Command(BaseCommand):
    """
    Custom Django management command to demonstrate ORM queries.
    
    BEGINNER EXPLANATION:
    - This class inherits from BaseCommand, which provides Django command functionality
    - The handle() method is where our main logic goes
    - self.stdout.write() is like print() but better for Django commands
    """
    
    help = 'Demonstrates Django ORM queries for relationship_app models'

    def add_arguments(self, parser):
        """
        Add command line arguments to our command.
        
        This allows users to specify what they want to do:
        --create-data: Create sample data
        --demo: Run all demonstrations
        --author: Query books by specific author
        --library: Query books in specific library
        """
        parser.add_argument(
            '--create-data',
            action='store_true',
            help='Create sample data for testing',
        )
        parser.add_argument(
            '--demo',
            action='store_true',
            help='Run all query demonstrations',
        )
        parser.add_argument(
            '--author',
            type=str,
            help='Query books by specific author name',
        )
        parser.add_argument(
            '--library',
            type=str,
            help='List books in specific library',
        )

    def handle(self, *args, **options):
        """
        Main method that runs when the command is executed.
        
        BEGINNER EXPLANATION:
        - This method is called when you run: python manage.py run_queries
        - The options parameter contains any command line arguments
        - We check which options were provided and run the appropriate functions
        """
        self.stdout.write(
            self.style.SUCCESS('🚀 Django ORM Query Demonstration Tool')
        )
        self.stdout.write('=' * 60)

        # Create sample data if requested
        if options['create_data']:
            self.create_sample_data()

        # Run full demo if requested
        if options['demo']:
            self.run_full_demo()

        # Query books by author if specified
        if options['author']:
            self.query_books_by_author(options['author'])

        # Query books in library if specified
        if options['library']:
            self.list_books_in_library(options['library'])

        # If no specific options, show help
        if not any([options['create_data'], options['demo'], 
                   options['author'], options['library']]):
            self.show_usage_help()

    def create_sample_data(self):
        """Create sample data for testing."""
        self.stdout.write('\n🏗️  Creating sample data...')
        
        # Create authors
        author1, created = Author.objects.get_or_create(name="J.K. Rowling")
        if created:
            self.stdout.write('   ✅ Created author: J.K. Rowling')
        else:
            self.stdout.write('   ♻️  Author already exists: J.K. Rowling')

        author2, created = Author.objects.get_or_create(name="George Orwell")
        if created:
            self.stdout.write('   ✅ Created author: George Orwell')
        else:
            self.stdout.write('   ♻️  Author already exists: George Orwell')

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

        self.stdout.write('   ✅ Created books')

        # Create library
        library, created = Library.objects.get_or_create(name="Central Library")
        if created:
            self.stdout.write('   ✅ Created library: Central Library')
        else:
            self.stdout.write('   ♻️  Library already exists: Central Library')

        # Add books to library
        library.books.add(book1, book2, book3)
        self.stdout.write('   ✅ Added books to library')

        # Create librarian
        librarian, created = Librarian.objects.get_or_create(
            name="Alice Smith",
            library=library
        )
        if created:
            self.stdout.write('   ✅ Created librarian: Alice Smith')
        else:
            self.stdout.write('   ♻️  Librarian already exists: Alice Smith')

        self.stdout.write(
            self.style.SUCCESS('\n🎉 Sample data creation completed!')
        )

    def query_books_by_author(self, author_name):
        """Query all books by a specific author."""
        self.stdout.write(f'\n📚 Querying books by author: {author_name}')
        self.stdout.write('-' * 50)
        
        try:
            author = Author.objects.get(name=author_name)
            books = Book.objects.filter(author=author)
            
            if books.exists():
                self.stdout.write(f'Found {books.count()} book(s):')
                for i, book in enumerate(books, 1):
                    self.stdout.write(f'   {i}. {book.title}')
            else:
                self.stdout.write('No books found for this author.')
                
        except Author.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Author "{author_name}" not found.')
            )

    def list_books_in_library(self, library_name):
        """List all books in a specific library."""
        self.stdout.write(f'\n🏛️  Listing books in library: {library_name}')
        self.stdout.write('-' * 50)
        
        try:
            library = Library.objects.get(name=library_name)
            books = library.books.all()
            
            if books.exists():
                self.stdout.write(f'Found {books.count()} book(s):')
                for i, book in enumerate(books, 1):
                    self.stdout.write(f'   {i}. "{book.title}" by {book.author.name}')
            else:
                self.stdout.write('No books found in this library.')
                
        except Library.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Library "{library_name}" not found.')
            )

    def retrieve_librarian(self, library_name):
        """Retrieve librarian for a specific library."""
        try:
            library = Library.objects.get(name=library_name)
            librarian = library.librarian
            self.stdout.write(f'👨‍💼 Librarian: {librarian.name}')
            return librarian
        except Library.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Library "{library_name}" not found.')
            )
        except Librarian.DoesNotExist:
            self.stdout.write(
                self.style.WARNING(f'No librarian assigned to {library_name}.')
            )

    def run_full_demo(self):
        """Run all demonstrations."""
        self.stdout.write('\n🔍 Running full demonstration...')
        
        # First create sample data
        self.create_sample_data()
        
        # Then run all queries
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('QUERY DEMONSTRATIONS')
        self.stdout.write('=' * 60)
        
        # Demo 1: Books by author
        self.query_books_by_author("J.K. Rowling")
        self.query_books_by_author("George Orwell")
        
        # Demo 2: Books in library
        self.list_books_in_library("Central Library")
        
        # Demo 3: Librarian
        self.stdout.write('\n👨‍💼 Retrieving librarian for Central Library:')
        self.stdout.write('-' * 50)
        self.retrieve_librarian("Central Library")

    def show_usage_help(self):
        """Show usage examples."""
        self.stdout.write('\n📖 Usage Examples:')
        self.stdout.write('=' * 40)
        self.stdout.write('Create sample data:')
        self.stdout.write('   python manage.py run_queries --create-data')
        self.stdout.write('\nRun full demonstration:')
        self.stdout.write('   python manage.py run_queries --demo')
        self.stdout.write('\nQuery books by author:')
        self.stdout.write('   python manage.py run_queries --author "J.K. Rowling"')
        self.stdout.write('\nList books in library:')
        self.stdout.write('   python manage.py run_queries --library "Central Library"')
        self.stdout.write('\n💡 Tip: You can combine options!')
        self.stdout.write('   python manage.py run_queries --create-data --demo')

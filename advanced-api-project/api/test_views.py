"""
Comprehensive Unit Tests for Django REST Framework API Endpoints

This file contains tests for all Book API endpoints including:
- CRUD operations (Create, Read, Update, Delete)
- Filtering, searching, and ordering functionality
- Permission and authentication testing
- Edge cases and error handling

Test Structure:
- SetUp: Create test data before each test
- Test Methods: Individual test cases for specific functionality
- TearDown: Clean up after tests (handled automatically by Django)
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from api.models import Author, Book
import json


class BookAPITestCase(APITestCase):
    """
    Test case for Book API endpoints.
    
    This class tests all the Book-related API functionality including
    CRUD operations, filtering, searching, ordering, and permissions.
    """

    def setUp(self):
        """
        Set up test data before each test method.
        
        This method runs before EVERY test method and creates:
        - Test users (regular user and staff user)
        - Test authors
        - Test books
        - API client for making requests
        """
        # Create test users
        self.regular_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.staff_user = User.objects.create_user(
            username='staffuser',
            email='staff@example.com',
            password='staffpass123',
            is_staff=True
        )
        
        # Create test authors
        self.author1 = Author.objects.create(name='J.K. Rowling')
        self.author2 = Author.objects.create(name='George Orwell')
        self.author3 = Author.objects.create(name='Jane Austen')
        
        # Create test books
        self.book1 = Book.objects.create(
            title='Harry Potter and the Philosopher\'s Stone',
            publication_year=1997,
            author=self.author1
        )
        
        self.book2 = Book.objects.create(
            title='1984',
            publication_year=1949,
            author=self.author2
        )
        
        self.book3 = Book.objects.create(
            title='Pride and Prejudice',
            publication_year=1813,
            author=self.author3
        )
        
        # Set up API client
        self.client = APIClient()
        
        # Define URL endpoints for easy reference
        self.book_list_url = reverse('book-list')  # /api/books/
        self.book_create_url = reverse('book-create')  # /api/books/create/
        self.book_update_url = reverse('book-update')  # /api/books/update/
        self.book_delete_url = reverse('book-delete')  # /api/books/delete/
        self.book_list_create_url = reverse('book-list-create')  # /api/books/list-create/
        
    def test_book_list_view(self):
        """
        Test GET /api/books/ - List all books
        
        Should return:
        - Status code 200
        - List of all books in JSON format
        - No authentication required
        """
        response = self.client.get(self.book_list_url)
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response data
        self.assertEqual(len(response.data), 3)  # We created 3 books
        
        # Check that first book data is correct
        first_book = response.data[0]
        self.assertIn('id', first_book)
        self.assertIn('title', first_book)
        self.assertIn('publication_year', first_book)
        self.assertIn('author', first_book)
        
    def test_book_detail_view(self):
        """
        Test GET /api/books/<id>/ - Get specific book details
        
        Should return:
        - Status code 200 for existing book
        - Correct book data
        - Status code 404 for non-existent book
        """
        # Test existing book
        url = reverse('book-detail', kwargs={'pk': self.book1.id})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)
        self.assertEqual(response.data['publication_year'], self.book1.publication_year)
        
        # Test non-existent book
        url = reverse('book-detail', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_book_create_view_authenticated(self):
        """
        Test POST /api/books/create/ - Create new book (authenticated user)
        
        Should:
        - Allow authenticated users to create books
        - Return status code 201
        - Return the created book data
        - Actually create the book in database
        """
        # Authenticate as regular user
        self.client.force_authenticate(user=self.regular_user)
        
        book_data = {
            'title': 'New Test Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, book_data, format='json')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check response contains success message and book data
        self.assertIn('message', response.data)
        self.assertIn('book', response.data)
        self.assertEqual(response.data['book']['title'], 'New Test Book')
        
        # Check book was actually created in database
        self.assertTrue(Book.objects.filter(title='New Test Book').exists())
        
    def test_book_create_view_unauthenticated(self):
        """
        Test POST /api/books/create/ - Create new book (unauthenticated user)
        
        Should:
        - Deny access to unauthenticated users
        - Return status code 401 (Unauthorized)
        """
        book_data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, book_data, format='json')
        
        # Should be denied
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Book should not be created
        self.assertFalse(Book.objects.filter(title='Unauthorized Book').exists())
        
    def test_book_create_view_invalid_data(self):
        """
        Test POST /api/books/create/ - Create book with invalid data
        
        Should:
        - Return status code 400 for invalid data
        - Return validation errors
        """
        self.client.force_authenticate(user=self.regular_user)
        
        # Test with future publication year (should be invalid)
        book_data = {
            'title': 'Future Book',
            'publication_year': 3000,  # Invalid: future year
            'author': self.author1.id
        }
        
        response = self.client.post(self.book_create_url, book_data, format='json')
        
        # Should return validation error
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)
        
    def test_book_update_view_authenticated(self):
        """
        Test PUT/PATCH /api/books/update/ - Update existing book (authenticated)
        
        Should:
        - Allow authenticated users to update books
        - Return success message and updated data
        - Actually update the book in database
        """
        self.client.force_authenticate(user=self.regular_user)
        
        update_data = {
            'id': self.book1.id,
            'title': 'Updated Harry Potter Title',
            'publication_year': 1997,  # Keep same year
            'author': self.author1.id
        }
        
        response = self.client.put(self.book_update_url, update_data, format='json')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check response message
        self.assertIn('message', response.data)
        self.assertIn('updated successfully', response.data['message'])
        
        # Check book was actually updated in database
        updated_book = Book.objects.get(id=self.book1.id)
        self.assertEqual(updated_book.title, 'Updated Harry Potter Title')
        
    def test_book_update_view_future_year_validation(self):
        """
        Test PUT /api/books/update/ - Prevent updating to future year
        
        Should:
        - Reject updates with future publication year
        - Return status code 400
        - Return appropriate error message
        """
        self.client.force_authenticate(user=self.regular_user)
        
        update_data = {
            'id': self.book1.id,
            'publication_year': 3000  # Future year - should be rejected
        }
        
        response = self.client.put(self.book_update_url, update_data, format='json')
        
        # Should be rejected
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_book_delete_view_staff_user(self):
        """
        Test DELETE /api/books/delete/ - Delete book (staff user)
        
        Should:
        - Allow staff users to delete books
        - Return success message with book title
        - Actually remove book from database
        """
        self.client.force_authenticate(user=self.staff_user)
        
        delete_data = {'id': self.book1.id}
        book_title = self.book1.title  # Store title before deletion
        
        response = self.client.delete(self.book_delete_url, delete_data, format='json')
        
        # Check status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check success message includes book title
        self.assertIn('message', response.data)
        self.assertIn(book_title, response.data['message'])
        
        # Check book was actually deleted
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())
        
    def test_book_delete_view_regular_user(self):
        """
        Test DELETE /api/books/delete/ - Delete book (regular user)
        
        Should:
        - Deny access to regular (non-staff) users
        - Return status code 403 (Forbidden)
        - Not delete the book
        """
        self.client.force_authenticate(user=self.regular_user)
        
        delete_data = {'id': self.book1.id}
        
        response = self.client.delete(self.book_delete_url, delete_data, format='json')
        
        # Should be denied (regular users can't delete)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Book should still exist
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())

    def test_book_filtering_by_title(self):
        """
        Test GET /api/books/?title__icontains=harry - Filter books by title
        
        Should:
        - Return books that contain the search term in title
        - Return empty list if no matches found
        - Be case-insensitive
        """
        # Test filtering for 'harry' (should find Harry Potter book)
        response = self.client.get(self.book_list_url + '?title__icontains=harry')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('Harry Potter', response.data[0]['title'])
        
        # Test filtering for non-existent term
        response = self.client.get(self.book_list_url + '?title__icontains=nonexistent')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        
    def test_book_filtering_by_author(self):
        """
        Test GET /api/books/?author=<id> - Filter books by author ID
        Test GET /api/books/?author_name__icontains=<name> - Filter by author name
        
        Should:
        - Return books by specific author
        - Support filtering by author ID and name
        """
        # Filter by author ID
        response = self.client.get(self.book_list_url + f'?author={self.author1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['author'], self.author1.id)
        
        # Filter by author name (case-insensitive partial match)
        response = self.client.get(self.book_list_url + '?author_name__icontains=orwell')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
        
    def test_book_filtering_by_publication_year(self):
        """
        Test publication year filtering:
        - ?publication_year=<year> (exact match)
        - ?publication_year__gte=<year> (greater than or equal)
        - ?publication_year__lte=<year> (less than or equal)
        - ?publication_year__range=<start>,<end> (range)
        """
        # Exact year match
        response = self.client.get(self.book_list_url + '?publication_year=1949')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')
        
        # Books published after 1900
        response = self.client.get(self.book_list_url + '?publication_year__gte=1900')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # 1949 and 1997 books
        
        # Books published before 1900
        response = self.client.get(self.book_list_url + '?publication_year__lte=1900')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1813 book
        
        # Books in range 1900-2000
        response = self.client.get(self.book_list_url + '?publication_year__range=1900,2000')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_book_searching(self):
        """
        Test GET /api/books/?search=<term> - Search across title and author name
        
        Should:
        - Search in both title and author name fields
        - Be case-insensitive
        - Find partial matches
        """
        # Search for 'potter' (should find in title)
        response = self.client.get(self.book_list_url + '?search=potter')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertIn('Potter', response.data[0]['title'])
        
        # Search for 'austen' (should find in author name)
        response = self.client.get(self.book_list_url + '?search=austen')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Pride and Prejudice')
        
        # Search for non-existent term
        response = self.client.get(self.book_list_url + '?search=nonexistent')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
        
    def test_book_ordering(self):
        """
        Test ordering functionality:
        - ?ordering=title (A-Z)
        - ?ordering=-title (Z-A)
        - ?ordering=publication_year (oldest first)
        - ?ordering=-publication_year (newest first)
        """
        # Order by title A-Z
        response = self.client.get(self.book_list_url + '?ordering=title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))  # Should be in alphabetical order
        
        # Order by title Z-A
        response = self.client.get(self.book_list_url + '?ordering=-title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles, reverse=True))
        
        # Order by publication year (oldest first)
        response = self.client.get(self.book_list_url + '?ordering=publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years))
        
        # Order by publication year (newest first)
        response = self.client.get(self.book_list_url + '?ordering=-publication_year')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
        
    def test_combined_filtering_searching_ordering(self):
        """
        Test combining filtering, searching, and ordering in single request
        
        Should:
        - Apply all parameters correctly
        - Return results that match all criteria
        """
        # Search for books + filter by year + order by title
        params = '?search=a&publication_year__gte=1900&ordering=title'
        response = self.client.get(self.book_list_url + params)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Results should be ordered by title
        if len(response.data) > 1:
            titles = [book['title'] for book in response.data]
            self.assertEqual(titles, sorted(titles))
        
        # All results should have publication_year >= 1900
        for book in response.data:
            self.assertGreaterEqual(book['publication_year'], 1900)
            
    def test_book_list_create_view_permissions(self):
        """
        Test GET/POST /api/books/list-create/ - Combined view with IsAuthenticatedOrReadOnly
        
        Should:
        - Allow anyone to GET (read)
        - Allow only authenticated users to POST (create)
        """
        # Test GET without authentication (should work)
        response = self.client.get(self.book_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test POST without authentication (should fail)
        book_data = {
            'title': 'Unauthorized Book',
            'publication_year': 2023,
            'author': self.author1.id
        }
        response = self.client.post(self.book_list_create_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test POST with authentication (should work)
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(self.book_list_create_url, book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BookAPIEdgeCasesTest(APITestCase):
    """
    Test edge cases and error conditions for Book API.
    
    These tests ensure the API handles unusual or invalid inputs gracefully.
    """
    
    def setUp(self):
        """Set up test data for edge case testing."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name='Test Author')
        self.client = APIClient()
        
    def test_create_book_missing_required_fields(self):
        """
        Test creating book with missing required fields.
        
        Should return validation errors for missing fields.
        """
        self.client.force_authenticate(user=self.user)
        
        # Missing title
        book_data = {
            'publication_year': 2023,
            'author': self.author.id
        }
        response = self.client.post(reverse('book-create'), book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', str(response.data))
        
    def test_create_book_invalid_author(self):
        """
        Test creating book with non-existent author.
        
        Should return validation error.
        """
        self.client.force_authenticate(user=self.user)
        
        book_data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': 9999  # Non-existent author ID
        }
        response = self.client.post(reverse('book-create'), book_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_update_nonexistent_book(self):
        """
        Test updating a book that doesn't exist.
        
        Should return 404 Not Found.
        """
        self.client.force_authenticate(user=self.user)
        
        update_data = {
            'id': 9999,  # Non-existent book ID
            'title': 'Updated Title'
        }
        response = self.client.put(reverse('book-update'), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    def test_delete_nonexistent_book(self):
        """
        Test deleting a book that doesn't exist.
        
        Should return 404 Not Found.
        """
        staff_user = User.objects.create_user(
            username='staff', password='pass', is_staff=True
        )
        self.client.force_authenticate(user=staff_user)
        
        delete_data = {'id': 9999}
        response = self.client.delete(reverse('book-delete'), delete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class AuthorModelTest(TestCase):
    """
    Test the Author model functionality.
    
    Tests model creation, string representation, and relationships.
    """
    
    def test_author_creation(self):
        """Test creating an Author instance."""
        author = Author.objects.create(name='Test Author')
        self.assertEqual(author.name, 'Test Author')
        self.assertEqual(str(author), 'Test Author')
        
    def test_author_book_relationship(self):
        """Test the one-to-many relationship between Author and Book."""
        author = Author.objects.create(name='Test Author')
        book = Book.objects.create(
            title='Test Book',
            publication_year=2023,
            author=author
        )
        
        # Test forward relationship
        self.assertEqual(book.author, author)
        
        # Test reverse relationship
        self.assertIn(book, author.books.all())
        

class BookModelTest(TestCase):
    """
    Test the Book model functionality.
    """
    
    def test_book_creation(self):
        """Test creating a Book instance."""
        author = Author.objects.create(name='Test Author')
        book = Book.objects.create(
            title='Test Book',
            publication_year=2023,
            author=author
        )
        
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.publication_year, 2023)
        self.assertEqual(book.author, author)
        self.assertEqual(str(book), 'Test Book (2023)')
        
    def test_book_serializer_validation(self):
        """Test Book serializer validation (future year prevention)."""
        from api.serializers import BookSerializer
        
        author = Author.objects.create(name='Test Author')
        
        # Test valid data
        valid_data = {
            'title': 'Valid Book',
            'publication_year': 2023,
            'author': author.id
        }
        serializer = BookSerializer(data=valid_data)
        self.assertTrue(serializer.is_valid())
        
        # Test invalid data (future year)
        invalid_data = {
            'title': 'Future Book',
            'publication_year': 3000,
            'author': author.id
        }
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)

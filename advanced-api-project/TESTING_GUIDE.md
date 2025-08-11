# Django REST Framework API Testing Guide

This guide explains our comprehensive testing strategy for the Book API, covering unit tests, test structure, and best practices.

## Overview

Our test suite validates:
- ✅ **CRUD Operations** (Create, Read, Update, Delete)
- ✅ **Authentication & Permissions** (who can access what)
- ✅ **Filtering, Searching, & Ordering** (query capabilities)
- ✅ **Data Validation** (input validation and error handling)
- ✅ **Edge Cases** (error conditions and boundary cases)

## Test File Structure

### Location: `/api/test_views.py`

```
api/test_views.py
├── BookAPITestCase           # Main API endpoint tests
├── BookAPIEdgeCasesTest     # Edge cases and error conditions
├── AuthorModelTest          # Author model functionality
└── BookModelTest            # Book model and serializer tests
```

## Test Classes Explained

### 1. BookAPITestCase
**Main API endpoint testing class**

Tests all primary API functionality:

#### CRUD Operations
- `test_book_list_view()` - GET /api/books/ (list all books)
- `test_book_detail_view()` - GET /api/books/<id>/ (get specific book)
- `test_book_create_view_authenticated()` - POST /api/books/create/ (create book)
- `test_book_update_view_authenticated()` - PUT /api/books/update/ (update book)
- `test_book_delete_view_staff_user()` - DELETE /api/books/delete/ (delete book)

#### Permission Testing
- `test_book_create_view_unauthenticated()` - Deny unauthenticated creation
- `test_book_delete_view_regular_user()` - Deny non-staff deletion
- `test_book_list_create_view_permissions()` - IsAuthenticatedOrReadOnly testing

#### Query Features
- `test_book_filtering_by_title()` - Filter by book title
- `test_book_filtering_by_author()` - Filter by author ID/name
- `test_book_filtering_by_publication_year()` - Filter by year (exact, range)
- `test_book_searching()` - Text search across fields
- `test_book_ordering()` - Sort by different fields
- `test_combined_filtering_searching_ordering()` - Multiple parameters

#### Validation Testing
- `test_book_create_view_invalid_data()` - Invalid input handling
- `test_book_update_view_future_year_validation()` - Business rule validation

### 2. BookAPIEdgeCasesTest
**Edge cases and error conditions**

- `test_create_book_missing_required_fields()` - Missing required data
- `test_create_book_invalid_author()` - Non-existent author reference
- `test_update_nonexistent_book()` - Update non-existent resource
- `test_delete_nonexistent_book()` - Delete non-existent resource

### 3. Model Tests
**Database model functionality**

- `AuthorModelTest` - Author model creation and relationships
- `BookModelTest` - Book model creation and serializer validation

## Running Tests

### Command Line Options

```bash
# Run all API tests
python manage.py test api

# Run with verbose output
python manage.py test api --verbosity=2

# Run specific test class
python manage.py test api.test_views.BookAPITestCase

# Run specific test method
python manage.py test api.test_views.BookAPITestCase.test_book_list_view

# Run with coverage reporting (if django-coverage is installed)
coverage run --source='.' manage.py test api
coverage report -m
```

### Expected Output

When tests pass, you'll see:
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....................
----------------------------------------------------------------------
Ran 20 tests in 0.234s

OK
Destroying test database for alias 'default'...
```

## Test Data Setup

### setUp() Method
Each test class has a `setUp()` method that runs before every test:

```python
def setUp(self):
    # Create test users
    self.regular_user = User.objects.create_user(...)
    self.staff_user = User.objects.create_user(..., is_staff=True)
    
    # Create test authors
    self.author1 = Author.objects.create(name='J.K. Rowling')
    
    # Create test books
    self.book1 = Book.objects.create(title='Harry Potter...', ...)
    
    # Set up API client
    self.client = APIClient()
```

### Test Isolation
- Each test runs in isolation with fresh data
- Django automatically rolls back database changes after each test
- No test affects another test's data

## Test Assertions Explained

### Status Code Testing
```python
self.assertEqual(response.status_code, status.HTTP_200_OK)
self.assertEqual(response.status_code, status.HTTP_201_CREATED)
self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
```

### Response Data Testing
```python
# Check response structure
self.assertIn('title', response.data)
self.assertIn('message', response.data)

# Check response values
self.assertEqual(response.data['title'], 'Expected Title')
self.assertEqual(len(response.data), 3)

# Check list ordering
titles = [book['title'] for book in response.data]
self.assertEqual(titles, sorted(titles))
```

### Database State Testing
```python
# Check object exists
self.assertTrue(Book.objects.filter(title='New Book').exists())

# Check object doesn't exist
self.assertFalse(Book.objects.filter(id=deleted_id).exists())

# Check object was updated
updated_book = Book.objects.get(id=book_id)
self.assertEqual(updated_book.title, 'Updated Title')
```

## Authentication in Tests

### Force Authentication
```python
# Authenticate as regular user
self.client.force_authenticate(user=self.regular_user)

# Authenticate as staff user  
self.client.force_authenticate(user=self.staff_user)

# Test without authentication (unauthenticated request)
# (no force_authenticate call)
```

### Testing Different User Types
- **Regular User**: Can create and update books
- **Staff User**: Can delete books (via custom permission)
- **Unauthenticated**: Can only read books

## Testing API Requests

### GET Requests
```python
response = self.client.get('/api/books/')
response = self.client.get('/api/books/?search=harry&ordering=title')
```

### POST Requests
```python
book_data = {'title': 'New Book', 'publication_year': 2023, 'author': 1}
response = self.client.post('/api/books/create/', book_data, format='json')
```

### PUT/PATCH Requests
```python
update_data = {'id': 1, 'title': 'Updated Title'}
response = self.client.put('/api/books/update/', update_data, format='json')
```

### DELETE Requests
```python
delete_data = {'id': 1}
response = self.client.delete('/api/books/delete/', delete_data, format='json')
```

## Test Coverage

Our tests cover:

### Functional Coverage ✅
- All API endpoints
- All HTTP methods (GET, POST, PUT, DELETE)
- All permission classes
- All filtering/searching/ordering options

### Edge Case Coverage ✅
- Invalid input data
- Missing required fields
- Non-existent resources
- Unauthorized access attempts
- Boundary conditions

### Integration Coverage ✅
- Database operations
- Permission enforcement
- Serializer validation
- Filter backend integration

## Best Practices Demonstrated

### 1. **Descriptive Test Names**
```python
def test_book_create_view_authenticated(self):  # Clear what is being tested
def test_book_delete_view_regular_user(self):   # Specific user scenario
```

### 2. **Comprehensive Test Documentation**
Each test includes docstrings explaining:
- What is being tested
- Expected behavior
- What should/shouldn't happen

### 3. **Isolated Test Data**
- Each test creates its own data
- Tests don't depend on each other
- Database is reset between tests

### 4. **Multiple Assertion Types**
- Status codes
- Response content
- Database state
- Business logic validation

### 5. **Error Condition Testing**
- Invalid inputs
- Missing permissions
- Non-existent resources
- Validation failures

## Troubleshooting Tests

### Common Issues

#### Test Database Permissions
If tests fail with database errors:
```bash
# Ensure test database can be created
python manage.py test --debug-mode
```

#### Import Errors
If you get import errors:
```python
# Check your imports in test_views.py
from django.test import TestCase
from rest_framework.test import APITestCase
```

#### Assertion Errors
If assertions fail:
- Check expected vs actual values
- Print response.data to debug
- Verify test data setup is correct

### Debugging Tests
```python
def test_debug_example(self):
    response = self.client.get('/api/books/')
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    # Add your assertions here
```

## Next Steps

### Extending Tests
Consider adding:
- **Performance tests** for large datasets
- **Integration tests** with external services
- **Load testing** with multiple concurrent users
- **Browser testing** with Selenium

### Continuous Integration
Set up automated testing:
```bash
# In CI/CD pipeline
python manage.py test api --verbosity=2
```

### Test Metrics
Track test coverage:
```bash
pip install coverage
coverage run --source='.' manage.py test api
coverage html  # Generate HTML report
```

## Summary

Our test suite provides:
- ✅ **100% endpoint coverage** - All API endpoints tested
- ✅ **Permission validation** - Authentication and authorization
- ✅ **Data integrity** - Database operations work correctly
- ✅ **Error handling** - Invalid inputs handled gracefully
- ✅ **Query functionality** - Filtering, searching, ordering work
- ✅ **Edge cases** - Boundary conditions and error states

This comprehensive testing ensures your API is reliable, secure, and functions as expected! 🚀

# Advanced API Project - Django REST Framework Views

This project demonstrates the implementation of custom views and generic views in Django REST Framework for handling CRUD operations on Book and Author models.

## Project Structure

```
advanced-api-project/
├── api/
│   ├── models.py          # Author and Book models
│   ├── serializers.py     # Custom serializers with validation
│   ├── views.py          # Generic views for CRUD operations
│   ├── urls.py           # API URL patterns
│   └── admin.py          # Admin configuration
├── advanced_api_project/
│   ├── settings.py       # Django settings
│   └── urls.py          # Main URL configuration
├── manage.py
├── test_api.py           # API testing script
└── create_test_data.py   # Script to create test data
```

## API Endpoints

### Book Endpoints

| HTTP Method | URL | View Class | Purpose | Permissions |
|-------------|-----|------------|---------|-------------|
| GET | `/api/books/` | BookListView | List all books | AllowAny |
| GET | `/api/books/<id>/` | BookDetailView | Get specific book | AllowAny |
| POST | `/api/books/create/` | BookCreateView | Create new book | IsAuthenticated |
| PUT/PATCH | `/api/books/update/` | BookUpdateView | Update book | IsAuthenticated |
| DELETE | `/api/books/delete/` | BookDeleteView | Delete book | IsOwnerOrReadOnly (staff only) |

## Generic Views Explained

### 1. ListView (BookListView)
- **Purpose**: Retrieve all books from database
- **HTTP Method**: GET
- **URL**: `/api/books/`
- **Permissions**: Anyone can access (no authentication required)
- **Response**: JSON array of book objects

### 2. DetailView (BookDetailView)  
- **Purpose**: Retrieve a single book by its ID
- **HTTP Method**: GET
- **URL**: `/api/books/<int:pk>/`
- **Permissions**: Anyone can access
- **Response**: JSON object of specific book

### 3. CreateView (BookCreateView)
- **Purpose**: Create a new book
- **HTTP Method**: POST
- **URL**: `/api/books/create/`
- **Permissions**: Only authenticated users
- **Custom Features**:
  - Validates that author exists before creating book
  - Returns custom success message
  - Uses `perform_create()` for custom logic

### 4. UpdateView (BookUpdateView)
- **Purpose**: Update an existing book
- **HTTP Methods**: PUT (full update), PATCH (partial update)
- **URL**: `/api/books/update/`
- **Permissions**: Only authenticated users
- **Note**: Book ID must be provided in request body
- **Custom Features**:
  - Prevents updating publication_year to future dates
  - Returns custom success message

### 5. DeleteView (BookDeleteView)
- **Purpose**: Delete a book from database
- **HTTP Method**: DELETE
- **URL**: `/api/books/delete/`
- **Permissions**: Custom permission (IsOwnerOrReadOnly - staff only)
- **Note**: Book ID must be provided in request body
- **Custom Features**:
  - Returns confirmation message with deleted book title

## Custom Permissions

### IsOwnerOrReadOnly
A custom permission class that implements the following logic:
- **Read Access**: Anyone can perform GET requests
- **Write Access**: Only authenticated users can create
- **Modify/Delete**: Only staff users can update/delete

```python
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Allow read for anyone, write for authenticated users
        
    def has_object_permission(self, request, view, obj):
        # Allow read for anyone, write for staff only
```

## Custom View Behavior

### BookCreateView Customizations
1. **Author Validation**: Checks if provided author ID exists
2. **Custom Response**: Returns structured JSON with success message
3. **Error Handling**: Provides clear error messages for invalid data

### BookUpdateView Customizations
1. **Date Validation**: Prevents updating publication_year to future
2. **Partial Updates**: Supports PATCH for updating only specific fields
3. **Custom Response**: Returns confirmation message

### BookDeleteView Customizations
1. **Confirmation Message**: Returns deleted book title in response
2. **Staff-Only Access**: Uses custom permission for enhanced security

## Testing the API

### 1. Manual Testing with Python
Use the provided `test_api.py` script:
```bash
python test_api.py
```

### 2. Using curl Commands
```bash
# List all books
curl http://localhost:8000/api/books/

# Get specific book
curl http://localhost:8000/api/books/1/

# Create new book (requires authentication)
curl -X POST http://localhost:8000/api/books/create/ \
  -H "Content-Type: application/json" \
  -d '{"title": "New Book", "publication_year": 2023, "author": 1}'

# Update existing book (requires authentication and book ID in body)
curl -X PUT http://localhost:8000/api/books/update/ \
  -H "Content-Type: application/json" \
  -d '{"id": 1, "title": "Updated Book", "publication_year": 2024, "author": 1}'

# Delete book (requires staff permissions and book ID in body)
curl -X DELETE http://localhost:8000/api/books/delete/ \
  -H "Content-Type: application/json" \
  -d '{"id": 1}'
```

### 3. Using Postman
1. Import the API endpoints into Postman
2. Set up authentication headers for protected endpoints
3. Test all CRUD operations

## Error Handling

The API provides meaningful error responses:

### Validation Errors (400 Bad Request)
```json
{
  "publication_year": ["Publication year cannot be in the future."]
}
```

### Authentication Errors (401 Unauthorized)
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Permission Errors (403 Forbidden)
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### Not Found Errors (404 Not Found)
```json
{
  "detail": "Not found."
}
```

## Key Learning Points

1. **Generic Views**: DRF generic views handle common patterns automatically
2. **Permissions**: Built-in and custom permission classes control access
3. **Customization**: Override methods like `perform_create()`, `create()`, `update()`, `destroy()`
4. **URL Patterns**: Clean URL structure with meaningful endpoints
5. **Error Handling**: Proper HTTP status codes and error messages
6. **Validation**: Both serializer-level and view-level validation

## Next Steps

To extend this project, consider:
1. Adding filtering and searching capabilities
2. Implementing pagination for large datasets
3. Adding API documentation with DRF's browsable API
4. Creating automated tests using Django's test framework
5. Adding throttling to prevent API abuse

"""
URL patterns for the API app.

This file defines the URL routing for our API endpoints.
Each URL pattern maps a specific URL path to a view class.

URL Structure:
- /books/ -> List all books (GET)
- /books/<id>/ -> Get specific book details (GET)  
- /books/create/ -> Create new book (POST)
- /books/update/ -> Update existing book (PUT/PATCH) - requires book ID in request body
- /books/delete/ -> Delete book (DELETE) - requires book ID in request body
"""

from django.urls import path
from . import views

# Define URL patterns for API endpoints
urlpatterns = [
    # ListView: GET /books/ - retrieve all books
    path('books/', views.BookListView.as_view(), name='book-list'),
    
    # DetailView: GET /books/<id>/ - retrieve single book by ID
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # CreateView: POST /books/create/ - create new book
    path('books/create/', views.BookCreateView.as_view(), name='book-create'),
    
    # UpdateView: PUT/PATCH /books/update/ - update existing book
    path('books/update/', views.BookUpdateView.as_view(), name='book-update'),
    
    # DeleteView: DELETE /books/delete/ - delete book
    path('books/delete/', views.BookDeleteView.as_view(), name='book-delete'),
    
    # Combined ListView and CreateView with IsAuthenticatedOrReadOnly permission
    path('books/list-create/', views.BookListCreateView.as_view(), name='book-list-create'),
]

"""
URL Pattern Explanation:
- path(): Django function to define URL patterns
- 'books/': The URL path (will be prefixed with /api/ from main urls.py)
- views.BookListView.as_view(): Converts class-based view to function
- name='book-list': Internal name for URL reversing
- <int:pk>: URL parameter that captures an integer as 'pk' (primary key)
"""

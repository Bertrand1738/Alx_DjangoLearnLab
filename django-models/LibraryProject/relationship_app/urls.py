"""
URL Configuration for relationship_app

BEGINNER EXPLANATION:
- URLs are like addresses for your website
- When someone visits /books/, Django looks here to find which view to run
- urlpatterns is a list of URL patterns Django checks in order
- path() connects a URL pattern to a view function or class
"""

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views  
from .views import list_books

# Define the app name for namespacing URLs
app_name = 'relationship_app'

urlpatterns = [
    # Function-based view for listing all books
    # URL: /books/
    # When someone visits this URL, run the list_books function
    path('books/', list_books, name='list_books'),

    # Class-based view for library details
    # URL: /library/1/ (where 1 is the library ID)
    # <int:pk> means capture an integer and pass it as 'pk' parameter
    # pk = primary key (the ID of the library)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
    
    # Authentication URLs
    # URL: /login/ - User login page using Django's built-in LoginView
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    
    # URL: /logout/ - User logout page using Django's built-in LogoutView
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    
    # URL: /register/ - User registration page
    path('register/', views.register, name='register'),
    
    # Role-based access control URLs
    # URL: /admin_view/ - Admin-only page
    path('admin_view/', views.admin_view, name='admin_view'),
    
    # URL: /librarian_view/ - Librarian-only page  
    path('librarian_view/', views.librarian_view, name='librarian_view'),
    
    # URL: /member_view/ - Member-only page
    path('member_view/', views.member_view, name='member_view'),
    
    # =============================================================================
    # CUSTOM PERMISSIONS-BASED URLS
    # =============================================================================
    
    # URL: /books_with_permissions/ - Enhanced book list with permission-based actions
    path('books_with_permissions/', views.book_list_with_permissions, name='book_list_with_permissions'),
    
    # URL: /add_book/ - Add new book (requires can_add_book permission)
    path('add_book/', views.add_book, name='add_book'),
    
    # URL: /edit_book/1/ - Edit book with ID 1 (requires can_change_book permission)
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    
    # URL: /delete_book/1/ - Delete book with ID 1 (requires can_delete_book permission)
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]

"""
HOW URLS WORK:
1. User visits: http://localhost:8000/relationship_app/books/
2. Django checks this file for matching patterns
3. Finds 'books/' pattern, calls views.list_books function
4. Function gets data, renders template, returns HTML to user

EXAMPLES:
- /books/ → Shows all books
- /library/1/ → Shows details for library with ID 1
- /library/2/ → Shows details for library with ID 2
"""

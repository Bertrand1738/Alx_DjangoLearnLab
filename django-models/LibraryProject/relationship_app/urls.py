"""
URL Configuration for relationship_app

BEGINNER EXPLANATION:
- URLs are like addresses for your website
- When someone visits /books/, Django looks here to find which view to run
- urlpatterns is a list of URL patterns Django checks in order
- path() connects a URL pattern to a view function or class
"""

from django.urls import path
from . import views

# Define the app name for namespacing URLs
app_name = 'relationship_app'

urlpatterns = [
    # Function-based view for listing all books
    # URL: /books/
    # When someone visits this URL, run the list_books function
    path('books/', views.list_books, name='list_books'),
    
    # Class-based view for library details
    # URL: /library/1/ (where 1 is the library ID)
    # <int:pk> means capture an integer and pass it as 'pk' parameter
    # pk = primary key (the ID of the library)
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
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

from django.urls import path
from . import views

urlpatterns = [
    # Book management URLs with permissions
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/edit/', views.book_edit, name='book_edit'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),
    
    # Utility URL to check permissions
    path('permissions/', views.check_permissions, name='check_permissions'),
]

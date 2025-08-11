"""
API Views for Book model using Django REST Framework Generic Views.

Generic Views provide pre-built functionality for common patterns:
- ListCreateAPIView: Combines listing all objects and creating new ones
- RetrieveUpdateDestroyAPIView: Combines retrieving, updating, and deleting single objects

These views automatically handle:
- Serialization/deserialization
- HTTP method routing (GET, POST, PUT, DELETE)
- Error handling
- Status codes

Permission Classes Explained:
- AllowAny: Anyone can access (no authentication required)
- IsAuthenticated: Only logged-in users can access
- IsAuthenticatedOrReadOnly: Anyone can read, only authenticated users can modify
"""

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission class that allows:
    - Anyone to read (GET requests)
    - Only authenticated users to create
    - Only the owner or staff to modify/delete
    
    This is an example of how to create custom permissions in DRF.
    """
    
    def has_permission(self, request, view):
        """
        Check if user has permission to access the view.
        """
        # Allow read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for authenticated users
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Check if user has permission to access specific object.
        """
        # Read permissions for anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions only for staff users (since books don't have owners)
        return request.user.is_staff


class BookListView(generics.ListAPIView):
    """
    ListView for retrieving all books.
    
    HTTP Method: GET
    URL: /books/
    Purpose: Returns a list of all books in the database
    Permissions: Anyone can view (no authentication required)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read


class BookDetailView(generics.RetrieveAPIView):
    """
    DetailView for retrieving a single book by ID.
    
    HTTP Method: GET  
    URL: /books/<int:pk>/
    Purpose: Returns details of a specific book
    Permissions: Anyone can view (no authentication required)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Anyone can read


class BookCreateView(generics.CreateAPIView):
    """
    CreateView for adding a new book.
    
    HTTP Method: POST
    URL: /books/create/
    Purpose: Creates a new book instance
    Permissions: Only authenticated users can create
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be logged in
    
    def perform_create(self, serializer):
        """
        Custom method called when creating a new book.
        This is where you can add custom logic before saving.
        """
        # Custom validation: Check if author exists
        author_id = self.request.data.get('author')
        if author_id:
            try:
                author = Author.objects.get(id=author_id)
            except Author.DoesNotExist:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({"author": "Author does not exist."})
        
        # Save the book
        serializer.save()
    
    def create(self, request, *args, **kwargs):
        """
        Override create method to add custom response.
        This method handles the entire creation process.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)  # Validate data
        self.perform_create(serializer)  # Call our custom perform_create
        
        # Return custom success response
        return Response({
            'message': 'Book created successfully!',
            'book': serializer.data
        }, status=status.HTTP_201_CREATED)


class BookUpdateView(generics.UpdateAPIView):
    """
    UpdateView for modifying an existing book.
    
    HTTP Method: PUT (full update) or PATCH (partial update)
    URL: /books/update/
    Purpose: Updates an existing book
    Permissions: Only authenticated users can update
    Note: Book ID should be provided in the request data
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Must be logged in
    
    def get_object(self):
        """
        Override get_object to get book by ID from request data instead of URL
        """
        book_id = self.request.data.get('id')
        if not book_id:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"id": "Book ID is required in request data."})
        
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound("Book not found.")
    
    def update(self, request, *args, **kwargs):
        """
        Override update method to add custom logic.
        """
        # Get the book instance using our custom get_object method
        instance = self.get_object()
        
        # Check if trying to update publication_year to future
        if 'publication_year' in request.data:
            from datetime import datetime
            if request.data['publication_year'] > datetime.now().year:
                return Response(
                    {'error': 'Cannot update publication year to future date'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        # Proceed with normal update
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            'message': 'Book updated successfully!',
            'book': serializer.data
        })


class BookDeleteView(generics.DestroyAPIView):
    """
    DeleteView for removing a book.
    
    HTTP Method: DELETE
    URL: /books/delete/
    Purpose: Deletes a book from the database
    Permissions: Only staff users can delete (using custom permission)
    Note: Book ID should be provided in the request data
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsOwnerOrReadOnly]  # Custom permission
    
    def get_object(self):
        """
        Override get_object to get book by ID from request data instead of URL
        """
        book_id = self.request.data.get('id')
        if not book_id:
            from rest_framework.exceptions import ValidationError
            raise ValidationError({"id": "Book ID is required in request data."})
        
        try:
            return Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            from rest_framework.exceptions import NotFound
            raise NotFound("Book not found.")
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy method to add custom response.
        """
        instance = self.get_object()
        book_title = instance.title  # Store title before deletion
        self.perform_destroy(instance)
        
        return Response({
            'message': f'Book "{book_title}" was deleted successfully!'
        }, status=status.HTTP_200_OK)

from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Book, Library

# Create your views here.

def list_books(request):
    """
    Function-based view to list all books.
    
    BEGINNER EXPLANATION:
    - This is a simple Python function that takes a 'request' parameter
    - request = information about the user's web request (GET, POST, etc.)
    - We get all books from the database using Book.objects.all()
    - We pass the books to a template to display them nicely
    - render() combines the template with the data and returns HTML
    """
    # Get all books from the database
    books = Book.objects.all()
    
    # Create a context dictionary to pass data to the template
    # The template will access this as {{ books }}
    context = {
        'books': books
    }
    
    # Render the template with the data
    # render(request, template_name, context)
    return render(request, 'relationship_app/list_books.html', context)


class LibraryDetailView(DetailView):
    """
    Class-based view to display details of a specific library.
    
    BEGINNER EXPLANATION:
    - This inherits from Django's DetailView class
    - DetailView automatically handles getting one object from the database
    - We just need to specify which model and template to use
    - Django automatically creates a context variable with the object
    - The object will be available in the template as {{ library }}
    """
    
    # Specify which model this view is for
    model = Library
    
    # Specify which template to use
    template_name = 'relationship_app/library_detail.html'
    
    # Specify the context variable name (optional, defaults to 'library')
    context_object_name = 'library'
    
    # Optional: Add extra context if needed
    def get_context_data(self, **kwargs):
        """
        Add extra data to the template context.
        
        BEGINNER EXPLANATION:
        - This method runs before rendering the template
        - We can add extra variables that the template can use
        - kwargs contains the default context (including our library object)
        """
        # Get the default context from the parent class
        context = super().get_context_data(**kwargs)
        
        # Add any extra context variables here if needed
        # For example: context['extra_info'] = 'Some extra information'
        
        return context

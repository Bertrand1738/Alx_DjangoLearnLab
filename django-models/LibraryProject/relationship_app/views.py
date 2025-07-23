from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from .models import Book
from .models import Library

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


# =============================================================================
# USER AUTHENTICATION VIEWS
# =============================================================================

def register(request):
    """
    Function-based view for user registration.
    
    BEGINNER EXPLANATION:
    - This view handles user registration (creating new accounts)
    - GET request: Shows the registration form
    - POST request: Processes the form and creates a new user
    - UserCreationForm is Django's built-in registration form
    - After successful registration, user is automatically logged in
    """
    if request.method == 'POST':
        # User submitted the registration form
        form = UserCreationForm(request.POST)
        
        if form.is_valid():
            # Form data is valid, create the user
            user = form.save()
            
            # Automatically log in the newly registered user
            login(request, user)
            
            # Redirect to a success page (you can change this URL)
            return redirect('relationship_app:list_books')
    else:
        # GET request: Show empty registration form
        form = UserCreationForm()
    
    # Render the registration template with the form
    return render(request, 'relationship_app/register.html', {'form': form})


class CustomLoginView(LoginView):
    """
    Class-based view for user login.
    
    BEGINNER EXPLANATION:
    - This inherits from Django's built-in LoginView
    - LoginView handles all the login logic for us
    - We just need to specify which template to use
    - Django automatically handles form validation and user authentication
    """
    template_name = 'relationship_app/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        """
        Where to redirect after successful login.
        """
        return '/relationship_app/books/'


class CustomLogoutView(LogoutView):
    """
    Class-based view for user logout.
    
    BEGINNER EXPLANATION:
    - This inherits from Django's built-in LogoutView
    - LogoutView handles clearing the user's session
    - We just specify which template to show after logout
    """
    template_name = 'relationship_app/logout.html'

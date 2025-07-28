from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test, permission_required
from django.contrib.auth.decorators import permission_required
from .models import Book, Library, Author

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

"""
AUTHENTICATION IMPLEMENTATION NOTE:
We use two approaches for authentication in this project:

1. BUILT-IN VIEWS (Used in URLs):
   - LoginView.as_view(template_name='...') in urls.py
   - LogoutView.as_view(template_name='...') in urls.py
   - These are Django's ready-made authentication views

2. CUSTOM VIEWS (Examples below):
   - Custom classes that inherit from Django's views
   - Useful when you need to customize behavior
"""

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


# =============================================================================
# ROLE-BASED ACCESS CONTROL VIEWS
# =============================================================================

def check_role(user, role):
    """
    Helper function to check if user has a specific role.
    
    BEGINNER EXPLANATION:
    - This function checks if a user has the required role
    - Returns True if user has the role, False otherwise
    - Used by the @user_passes_test decorator below
    """
    return hasattr(user, 'userprofile') and user.userprofile.role == role


# Role checking functions for decorators
def is_admin(user):
    """Check if user has Admin role"""
    return check_role(user, 'Admin')


def is_librarian(user):
    """Check if user has Librarian role"""
    return check_role(user, 'Librarian')


def is_member(user):
    """Check if user has Member role"""
    return check_role(user, 'Member')


@user_passes_test(is_admin)
def admin_view(request):
    """
    Admin-only view accessible only to users with 'Admin' role.
    
    BEGINNER EXPLANATION:
    - @user_passes_test decorator checks if user passes the is_admin test
    - If user is not Admin, they get redirected to login page
    - Only Admin users can see this page and its content
    """
    return render(request, 'relationship_app/admin_view.html', {
        'message': 'Welcome to the Admin Panel!',
        'user_role': request.user.userprofile.role,
    })


@user_passes_test(is_librarian)
def librarian_view(request):
    """
    Librarian-only view accessible only to users with 'Librarian' role.
    
    BEGINNER EXPLANATION:
    - Only users with 'Librarian' role can access this view
    - Librarians can manage books and see library statistics
    - Non-librarians are redirected to login page
    """
    return render(request, 'relationship_app/librarian_view.html', {
        'message': 'Welcome to the Librarian Dashboard!',
        'user_role': request.user.userprofile.role,
        'books': Book.objects.all(),  # Show all books to librarians
    })


@user_passes_test(is_member)
def member_view(request):
    """
    Member-only view accessible only to users with 'Member' role.
    
    BEGINNER EXPLANATION:
    - Only users with 'Member' role can access this view
    - Members can browse books but have limited permissions
    - Non-members are redirected to login page
    """
    return render(request, 'relationship_app/member_view.html', {
        'message': 'Welcome to the Member Area!',
        'user_role': request.user.userprofile.role,
        'books': Book.objects.all()[:5],  # Show only first 5 books to members
    })


# =============================================================================
# CUSTOM PERMISSIONS-BASED VIEWS
# =============================================================================

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    View for adding a new book - requires 'can_add_book' permission.
    
    BEGINNER EXPLANATION:
    - @permission_required decorator checks if user has specific permission
    - Only users with 'can_add_book' permission can access this view
    - raise_exception=True means users without permission get a 403 error
    - This view handles both showing the form (GET) and processing it (POST)
    """
    if request.method == 'POST':
        # User submitted the form to add a book
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        
        if title and author_id:
            try:
                author = Author.objects.get(id=author_id)
                book = Book.objects.create(title=title, author=author)
                return redirect('relationship_app:list_books')
            except Author.DoesNotExist:
                error = "Selected author does not exist."
        else:
            error = "Title and author are required."
        
        return render(request, 'relationship_app/add_book.html', {
            'authors': Author.objects.all(),
            'error': error,
        })
    else:
        # GET request: Show the add book form
        return render(request, 'relationship_app/add_book.html', {
            'authors': Author.objects.all(),
        })


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, book_id):
    """
    View for editing an existing book - requires 'can_change_book' permission.
    
    BEGINNER EXPLANATION:
    - Only users with 'can_change_book' permission can edit books
    - book_id parameter comes from the URL pattern
    - get_object_or_404 gets the book or shows 404 if not found
    - Form shows current values and allows updating them
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        # User submitted the form to update the book
        title = request.POST.get('title')
        author_id = request.POST.get('author')
        
        if title and author_id:
            try:
                author = Author.objects.get(id=author_id)
                book.title = title
                book.author = author
                book.save()
                return redirect('relationship_app:list_books')
            except Author.DoesNotExist:
                error = "Selected author does not exist."
        else:
            error = "Title and author are required."
        
        return render(request, 'relationship_app/edit_book.html', {
            'book': book,
            'authors': Author.objects.all(),
            'error': error,
        })
    else:
        # GET request: Show the edit form with current values
        return render(request, 'relationship_app/edit_book.html', {
            'book': book,
            'authors': Author.objects.all(),
        })


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    """
    View for deleting a book - requires 'can_delete_book' permission.
    
    BEGINNER EXPLANATION:
    - Only users with 'can_delete_book' permission can delete books
    - Shows confirmation page (GET) before actually deleting (POST)
    - This two-step process prevents accidental deletions
    - After deletion, redirects back to book list
    """
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        # User confirmed deletion
        book.delete()
        return redirect('relationship_app:list_books')
    else:
        # GET request: Show confirmation page
        return render(request, 'relationship_app/delete_book.html', {
            'book': book,
        })


def book_list_with_permissions(request):
    """
    Enhanced book list view that shows permission-based action buttons.
    
    BEGINNER EXPLANATION:
    - This view shows all books like list_books()
    - Additionally, it checks what permissions the current user has
    - Template can show/hide Add/Edit/Delete buttons based on permissions
    - Uses user.has_perm() to check specific permissions
    """
    books = Book.objects.all()
    
    # Check user's permissions for the template
    user_permissions = {
        'can_add': request.user.has_perm('relationship_app.can_add_book'),
        'can_change': request.user.has_perm('relationship_app.can_change_book'),
        'can_delete': request.user.has_perm('relationship_app.can_delete_book'),
    }
    
    return render(request, 'relationship_app/book_list_with_permissions.html', {
        'books': books,
        'permissions': user_permissions,
    })

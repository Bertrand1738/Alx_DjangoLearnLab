from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.html import escape
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from .models import Book
from .forms import BookForm, BookSearchForm, ExampleForm
import logging

# Set up security logging
security_logger = logging.getLogger('django.security')

# Create your views here.

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Secure view to display books with search functionality.
    Requires 'can_view' permission.
    
    SECURITY FEATURES:
    - Uses Django ORM to prevent SQL injection
    - Validates search input through forms
    - Implements pagination to prevent DoS
    - Logs security events
    """
    # Initialize search form
    search_form = BookSearchForm(request.GET or None)
    books = Book.objects.all()
    
    # Handle search with security validation
    if search_form.is_valid() and search_form.cleaned_data.get('query'):
        query = search_form.cleaned_data['query']
        search_type = search_form.cleaned_data.get('search_type', 'all')
        
        # Log search attempt
        security_logger.info(f"User {request.user.username} searched for: {query}")
        
        # Secure search using Django ORM (prevents SQL injection)
        if search_type == 'title':
            books = books.filter(title__icontains=query)
        elif search_type == 'author':
            books = books.filter(author__icontains=query)
        else:  # search_type == 'all'
            books = books.filter(
                Q(title__icontains=query) | Q(author__icontains=query)
            )
        
        # Add message about search results
        count = books.count()
        messages.info(request, f"Found {count} book(s) matching '{escape(query)}'")
    
    # Implement pagination to prevent DoS attacks
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page', 1)
    
    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1
    except (ValueError, TypeError):
        page_number = 1
    
    books_page = paginator.get_page(page_number)
    
    context = {
        'books': books_page,
        'search_form': search_form,
        'total_books': paginator.count,
    }
    
    return render(request, 'bookshelf/book_list.html', context)


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_create(request):
    """
    Secure view to create a new book.
    Requires 'can_create' permission.
    
    SECURITY FEATURES:
    - Uses Django forms for validation and sanitization
    - CSRF protection decorator
    - Restricts HTTP methods
    - Logs creation events
    """
    if request.method == 'POST':
        form = BookForm(request.POST)
        
        if form.is_valid():
            try:
                # Create book using validated data
                book = form.save()
                
                # Log successful creation
                security_logger.info(
                    f"User {request.user.username} created book: {book.title}"
                )
                
                messages.success(
                    request, 
                    f'Book "{escape(book.title)}" created successfully!'
                )
                return redirect('book_list')
                
            except Exception as e:
                # Log error for security monitoring
                security_logger.error(
                    f"Error creating book by user {request.user.username}: {str(e)}"
                )
                messages.error(request, 'An error occurred while creating the book.')
        else:
            # Log validation errors for security monitoring
            security_logger.warning(
                f"User {request.user.username} submitted invalid book form: {form.errors}"
            )
    else:
        form = BookForm()
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form, 
        'action': 'Create'
    })


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_edit(request, pk):
    """
    Secure view to edit an existing book.
    Requires 'can_edit' permission.
    
    SECURITY FEATURES:
    - Uses get_object_or_404 to prevent unauthorized access
    - Django forms for validation
    - CSRF protection
    - Activity logging
    """
    # Securely get book or return 404
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        
        if form.is_valid():
            try:
                # Store old values for logging
                old_title = book.title
                
                # Save with validated data
                updated_book = form.save()
                
                # Log the edit
                security_logger.info(
                    f"User {request.user.username} edited book {pk}: "
                    f"'{old_title}' -> '{updated_book.title}'"
                )
                
                messages.success(
                    request, 
                    f'Book "{escape(updated_book.title)}" updated successfully!'
                )
                return redirect('book_list')
                
            except Exception as e:
                security_logger.error(
                    f"Error editing book {pk} by user {request.user.username}: {str(e)}"
                )
                messages.error(request, 'An error occurred while updating the book.')
        else:
            security_logger.warning(
                f"User {request.user.username} submitted invalid edit form for book {pk}: {form.errors}"
            )
    else:
        form = BookForm(instance=book)
    
    return render(request, 'bookshelf/book_form.html', {
        'form': form,
        'book': book,
        'action': 'Edit'
    })


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
@csrf_protect
@require_http_methods(["GET", "POST"])
def book_delete(request, pk):
    """
    Secure view to delete a book.
    Requires 'can_delete' permission.
    
    SECURITY FEATURES:
    - Double confirmation required
    - Secure object retrieval
    - Activity logging
    - CSRF protection
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        # Store details for logging before deletion
        book_title = book.title
        book_author = book.author
        
        try:
            book.delete()
            
            # Log the deletion
            security_logger.warning(
                f"User {request.user.username} deleted book {pk}: "
                f"'{book_title}' by {book_author}"
            )
            
            messages.success(
                request, 
                f'Book "{escape(book_title)}" deleted successfully!'
            )
            return redirect('book_list')
            
        except Exception as e:
            security_logger.error(
                f"Error deleting book {pk} by user {request.user.username}: {str(e)}"
            )
            messages.error(request, 'An error occurred while deleting the book.')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


@login_required
def check_permissions(request):
    """
    Helper view to check what permissions a user has.
    Enhanced with security information.
    """
    user_permissions = {
        'can_view': request.user.has_perm('bookshelf.can_view'),
        'can_create': request.user.has_perm('bookshelf.can_create'),
        'can_edit': request.user.has_perm('bookshelf.can_edit'),
        'can_delete': request.user.has_perm('bookshelf.can_delete'),
    }
    
    user_groups = request.user.groups.all()
    
    # Log permission check for security monitoring
    security_logger.info(
        f"User {request.user.username} checked permissions. "
        f"Groups: {[g.name for g in user_groups]}"
    )
    
    # Add security headers to response
    context = {
        'user_permissions': user_permissions,
        'user_groups': user_groups,
        'security_info': {
            'csrf_token_valid': request.META.get('CSRF_COOKIE') is not None,
            'is_secure': request.is_secure(),
            'session_age': request.session.get_expiry_age(),
        }
    }
    
    response = render(request, 'bookshelf/permissions_check.html', context)
    
    # Add security headers
    response['X-Content-Type-Options'] = 'nosniff'
    response['X-Frame-Options'] = 'DENY'
    
    return response


@login_required
@csrf_protect
@require_http_methods(["GET", "POST"])
def example_form_view(request):
    """
    Example view demonstrating secure form handling.
    
    SECURITY FEATURES DEMONSTRATED:
    - CSRF protection
    - Input validation through Django forms
    - XSS prevention
    - Security logging
    - Proper error handling
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        
        if form.is_valid():
            # Process the validated data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data.get('message', '')
            
            # Log the form submission
            security_logger.info(
                f"User {request.user.username} submitted example form. "
                f"Name: {name}, Email: {email}"
            )
            
            # In a real application, you might save to database or send email
            messages.success(
                request,
                f'Thank you {escape(name)}! Your form has been submitted successfully.'
            )
            
            # Redirect to prevent form resubmission
            return redirect('example_form')
            
        else:
            # Log validation errors for security monitoring
            security_logger.warning(
                f"User {request.user.username} submitted invalid example form: {form.errors}"
            )
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ExampleForm()
    
    return render(request, 'bookshelf/example_form.html', {'form': form})


# Class-based views for additional functionality

class BookSearchView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    """
    Secure search view for books using class-based view.
    
    SECURITY FEATURES:
    - Authentication required via LoginRequiredMixin
    - Permission checking via PermissionRequiredMixin
    - Query parameterization to prevent SQL injection
    - Input sanitization through Django forms
    """
    model = Book
    template_name = 'bookshelf/book_list.html'
    context_object_name = 'books'
    permission_required = 'bookshelf.can_view'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Override queryset to implement search functionality with security.
        """
        queryset = super().get_queryset()
        search_form = BookSearchForm(self.request.GET)
        
        if search_form.is_valid():
            query = search_form.cleaned_data.get('query')
            if query:
                # Log search query for security monitoring
                security_logger.info(
                    f"User {self.request.user.username} searched for: {query}"
                )
                
                # Secure search using Q objects (prevents SQL injection)
                queryset = queryset.filter(
                    Q(title__icontains=query) | 
                    Q(author__icontains=query)
                )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        """
        Add search form to context.
        """
        context = super().get_context_data(**kwargs)
        context['search_form'] = BookSearchForm(self.request.GET)
        return context


class BookDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """
    Secure delete view for books.
    
    SECURITY FEATURES:
    - Authentication required via LoginRequiredMixin
    - Permission checking via PermissionRequiredMixin
    - CSRF protection (built into DeleteView)
    - Confirmation template to prevent accidental deletion
    - Security logging for audit trail
    """
    model = Book
    template_name = 'bookshelf/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')
    permission_required = 'bookshelf.can_delete'
    
    def delete(self, request, *args, **kwargs):
        """
        Override delete method to add security logging.
        """
        book = self.get_object()
        
        # Log the deletion for security audit trail
        security_logger.info(
            f"User {request.user.username} deleted book: "
            f"'{book.title}' by {book.author} (ID: {book.pk})"
        )
        
        # Call parent delete method
        response = super().delete(request, *args, **kwargs)
        
        # Add success message
        messages.success(
            request, 
            f'Book "{escape(book.title)}" has been successfully deleted.'
        )
        
        return response
    
    def get_context_data(self, **kwargs):
        """
        Add additional security context to template.
        """
        context = super().get_context_data(**kwargs)
        context['security_note'] = (
            "This action cannot be undone. The book will be permanently removed."
        )
        return context


@login_required
@csrf_protect
def permissions_check(request):
    """
    View to display current user's permissions for security debugging.
    
    This view shows the user their current permissions, groups, and 
    access levels for security transparency and debugging.
    """
    user_permissions = []
    
    # Check specific book permissions
    permissions = ['can_view', 'can_create', 'can_edit', 'can_delete']
    for perm in permissions:
        full_perm = f'bookshelf.{perm}'
        has_perm = request.user.has_perm(full_perm)
        user_permissions.append({
            'permission': perm,
            'has_permission': has_perm,
            'full_name': full_perm
        })
    
    # Get user groups
    user_groups = request.user.groups.all()
    
    # Log the permission check for security monitoring
    security_logger.info(
        f"User {request.user.username} checked their permissions. "
        f"Groups: {[g.name for g in user_groups]}"
    )
    
    context = {
        'user_permissions': user_permissions,
        'user_groups': user_groups,
        'is_superuser': request.user.is_superuser,
        'is_staff': request.user.is_staff,
    }
    
    return render(request, 'bookshelf/permissions_check.html', context)


@login_required
def check_permissions(request):
    """
    Alternative permission check view that returns JSON for API usage.
    
    This can be used by frontend JavaScript for dynamic permission checking.
    """
    permissions_data = {
        'username': request.user.username,
        'is_authenticated': request.user.is_authenticated,
        'is_superuser': request.user.is_superuser,
        'is_staff': request.user.is_staff,
        'groups': [group.name for group in request.user.groups.all()],
        'permissions': {
            'can_view': request.user.has_perm('bookshelf.can_view'),
            'can_create': request.user.has_perm('bookshelf.can_create'),
            'can_edit': request.user.has_perm('bookshelf.can_edit'),
            'can_delete': request.user.has_perm('bookshelf.can_delete'),
        }
    }
    
    # Log API permission check
    security_logger.info(
        f"API permission check for user {request.user.username}"
    )
    
    return JsonResponse(permissions_data)

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .models import Book

# Create your views here.

@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    View to display all books.
    Requires 'can_view' permission.
    
    BEGINNER EXPLANATION:
    - @login_required: User must be logged in
    - @permission_required: User must have 'bookshelf.can_view' permission
    - raise_exception=True: Shows 403 error if permission denied
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@login_required
@permission_required('bookshelf.can_create', raise_exception=True)
def book_create(request):
    """
    View to create a new book.
    Requires 'can_create' permission.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        
        if title and author and publication_year:
            book = Book.objects.create(
                title=title,
                author=author,
                publication_year=int(publication_year)
            )
            messages.success(request, f'Book "{book.title}" created successfully!')
            return redirect('book_list')
        else:
            messages.error(request, 'All fields are required!')
    
    return render(request, 'bookshelf/book_form.html', {'action': 'Create'})


@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def book_edit(request, pk):
    """
    View to edit an existing book.
    Requires 'can_edit' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.publication_year = int(request.POST.get('publication_year', book.publication_year))
        book.save()
        
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_form.html', {
        'book': book, 
        'action': 'Edit'
    })


@login_required
@permission_required('bookshelf.can_delete', raise_exception=True)
def book_delete(request, pk):
    """
    View to delete a book.
    Requires 'can_delete' permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/book_confirm_delete.html', {'book': book})


@login_required
def check_permissions(request):
    """
    Helper view to check what permissions a user has.
    Useful for debugging and understanding user capabilities.
    """
    user_permissions = {
        'can_view': request.user.has_perm('bookshelf.can_view'),
        'can_create': request.user.has_perm('bookshelf.can_create'),
        'can_edit': request.user.has_perm('bookshelf.can_edit'),
        'can_delete': request.user.has_perm('bookshelf.can_delete'),
    }
    
    user_groups = request.user.groups.all()
    
    context = {
        'user_permissions': user_permissions,
        'user_groups': user_groups,
    }
    
    return render(request, 'bookshelf/permissions_check.html', context)

from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import Product
from django.shortcuts import get_object_or_404
from .forms import ProductForm, ProductSearchForm
from django.db.models import Q

def index(request):
    # Get some featured products (first 3)
    featured_products = Product.objects.all()[:3]
    total_products = Product.objects.count()
    categories_count = Product.objects.values_list('category', flat=True).distinct().count()
    
    context = {
        'featured_products': featured_products,
        'total_products': total_products,
        'categories_count': categories_count,
    }
    return render(request, 'book_store/index.html', context)

def products(request):
    # Get all products
    products = Product.objects.all()
    
    # Filter by category if specified in URL parameter
    category = request.GET.get('category')
    if category:
        products = products.filter(category=category)
    
    # Order by price (lowest first)
    products = products.order_by('price')
    
    # Get unique categories for filter buttons
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    context = {
        'products': products,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'book_store/products.html', context)

# Authentication Views
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

# Permission-protected views
@permission_required('book_store.can_manage_inventory', raise_exception=True)
def manage_inventory(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'can_add': request.user.has_perm('book_store.add_product'),
        'can_change': request.user.has_perm('book_store.change_product'),
        'can_delete': request.user.has_perm('book_store.delete_product'),
    }
    return render(request, 'book_store/manage_inventory.html', context)

@permission_required('book_store.can_set_prices', raise_exception=True)
def set_prices(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'book_store/set_prices.html', context)

@login_required
def feature_products(request):
    if not request.user.has_perm('book_store.can_view_all_products'):
        # Regular users see limited products
        products = Product.objects.all()[:3]
    else:
        # Users with permission see all products
        products = Product.objects.all()
    
    context = {'products': products}
    return render(request, 'book_store/feature_products.html', context)

@login_required
def delete_product(request, product_id):
    """View to delete a product - only for users with delete permission"""
    # Check if user has permission (custom or built-in) or is superuser
    if not (request.user.has_perm('book_store.can_delete_product') or 
            request.user.has_perm('book_store.delete_product') or 
            request.user.is_superuser):
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("You don't have permission to delete products")
    
    print(f"🔍 DELETE VIEW CALLED: Method={request.method}, Product ID={product_id}")
    print(f"🔍 User: {request.user.username}, Is Superuser: {request.user.is_superuser}")
    
    product = get_object_or_404(Product, id=product_id)
    print(f"🔍 Product found: {product.name}")
    
    if request.method == 'POST':
        print("🔍 POST request received - attempting to delete product")
        product_name = product.name
        product.delete()
        print(f"🔍 Product '{product_name}' deleted successfully")
        messages.success(request, f'Product "{product_name}" has been deleted successfully!')
        return redirect('products')
    
    print("🔍 GET request - showing confirmation page")
    context = {
        'product': product,
    }
    return render(request, 'book_store/delete_product.html', context)

# Secure Product Management Views
@login_required
@permission_required('book_store.add_product', raise_exception=True)
def add_product(request):
    """
    Secure view for adding new products with validation
    """
    print(f"🔍 ADD PRODUCT VIEW: Method={request.method}, User={request.user.username}")
    
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            print(f"✅ Product created: {product.name}")
            messages.success(request, f'Product "{product.name}" has been added successfully!')
            return redirect('products')
        else:
            print(f"❌ Form validation failed: {form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Add New Product'
    }
    return render(request, 'book_store/product_form.html', context)

@login_required
@permission_required('book_store.change_product', raise_exception=True)
def edit_product(request, product_id):
    """
    Secure view for editing existing products
    """
    product = get_object_or_404(Product, id=product_id)
    print(f"🔍 EDIT PRODUCT VIEW: Method={request.method}, Product={product.name}")
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            updated_product = form.save()
            print(f"✅ Product updated: {updated_product.name}")
            messages.success(request, f'Product "{updated_product.name}" has been updated successfully!')
            return redirect('products')
        else:
            print(f"❌ Form validation failed: {form.errors}")
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': f'Edit {product.name}'
    }
    return render(request, 'book_store/product_form.html', context)

def secure_products(request):
    """
    Enhanced products view with secure search functionality
    """
    # Initialize search form
    search_form = ProductSearchForm(request.GET)
    products = Product.objects.all()
    
    # Apply filters if form is valid
    if search_form.is_valid():
        query = search_form.cleaned_data.get('query')
        category = search_form.cleaned_data.get('category')
        min_price = search_form.cleaned_data.get('min_price')
        max_price = search_form.cleaned_data.get('max_price')
        
        # Apply search filters
        if query:
            products = products.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query)
            )
        
        if category:
            products = products.filter(category=category)
        
        if min_price:
            products = products.filter(price__gte=min_price)
        
        if max_price:
            products = products.filter(price__lte=max_price)
    
    # Order by price (lowest first)
    products = products.order_by('price')
    
    # Get unique categories for filter buttons
    categories = Product.objects.values_list('category', flat=True).distinct()
    
    context = {
        'products': products,
        'categories': categories,
        'search_form': search_form,
        'selected_category': request.GET.get('category'),
    }
    return render(request, 'book_store/secure_products.html', context)

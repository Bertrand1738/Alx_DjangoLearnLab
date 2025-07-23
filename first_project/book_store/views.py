from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.shortcuts import redirect
from .models import Product

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

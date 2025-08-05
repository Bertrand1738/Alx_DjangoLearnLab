"""
Django Forms with Security and Validation
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import Product
import re

class ProductForm(forms.ModelForm):
    """
    Secure form for creating/editing products with comprehensive validation
    """
    
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name',
                'maxlength': 100
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product description',
                'rows': 4,
                'maxlength': 1000
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category',
                'maxlength': 50
            })
        }
    
    def clean_name(self):
        """
        Custom validation for product name
        """
        name = self.cleaned_data.get('name')
        
        # Check if name is provided
        if not name:
            raise ValidationError("Product name is required.")
        
        # Remove extra whitespace
        name = name.strip()
        
        # Check minimum length
        if len(name) < 2:
            raise ValidationError("Product name must be at least 2 characters long.")
        
        # Check for only letters, numbers, spaces, and basic punctuation
        if not re.match(r'^[a-zA-Z0-9\s\-\'\":.,!?()]+$', name):
            raise ValidationError("Product name contains invalid characters. Only letters, numbers, spaces, and basic punctuation are allowed.")
        
        # Check for duplicate names (case-insensitive)
        if Product.objects.filter(name__iexact=name).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise ValidationError("A product with this name already exists.")
        
        return name
    
    def clean_description(self):
        """
        Custom validation for description
        """
        description = self.cleaned_data.get('description')
        
        if not description:
            raise ValidationError("Product description is required.")
        
        description = description.strip()
        
        # Check minimum length
        if len(description) < 10:
            raise ValidationError("Description must be at least 10 characters long.")
        
        # Check maximum length
        if len(description) > 1000:
            raise ValidationError("Description cannot exceed 1000 characters.")
        
        # Basic content validation - no excessive special characters
        special_char_count = len(re.findall(r'[^a-zA-Z0-9\s\-\'\":.,!?()]', description))
        if special_char_count > len(description) * 0.1:  # More than 10% special chars
            raise ValidationError("Description contains too many special characters.")
        
        return description
    
    def clean_price(self):
        """
        Custom validation for price
        """
        price = self.cleaned_data.get('price')
        
        if price is None:
            raise ValidationError("Price is required.")
        
        # Check if price is positive
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        
        # Check if price is reasonable (not too high)
        if price > 9999.99:
            raise ValidationError("Price cannot exceed $9,999.99.")
        
        # Check decimal places (max 2)
        if hasattr(price, 'as_tuple') and len(price.as_tuple().digits) - price.as_tuple().exponent > 2:
            raise ValidationError("Price cannot have more than 2 decimal places.")
        
        return price
    
    def clean_category(self):
        """
        Custom validation for category
        """
        category = self.cleaned_data.get('category')
        
        if not category:
            raise ValidationError("Category is required.")
        
        category = category.strip().title()  # Normalize to Title Case
        
        # Check length
        if len(category) < 2:
            raise ValidationError("Category must be at least 2 characters long.")
        
        # Only allow letters and spaces
        if not re.match(r'^[a-zA-Z\s]+$', category):
            raise ValidationError("Category can only contain letters and spaces.")
        
        # Predefined allowed categories for consistency
        allowed_categories = [
            'Programming', 'Web Development', 'Data Science', 'Machine Learning',
            'Database', 'Mobile Development', 'Development Tools', 'Computer Science',
            'Design', 'Business', 'Fiction', 'Non-Fiction', 'Education'
        ]
        
        if category not in allowed_categories:
            raise ValidationError(
                f"Please select from allowed categories: {', '.join(allowed_categories)}"
            )
        
        return category
    
    def clean(self):
        """
        Cross-field validation
        """
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        price = cleaned_data.get('price')
        category = cleaned_data.get('category')
        
        # Business logic validation
        if name and price:
            # If it's a premium category, enforce minimum price
            premium_categories = ['Computer Science', 'Machine Learning', 'Data Science']
            if category in premium_categories and price < 25.00:
                raise ValidationError(
                    f"{category} books must be priced at least $25.00 due to their specialized nature."
                )
        
        return cleaned_data


class ProductSearchForm(forms.Form):
    """
    Secure search form with validation
    """
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...',
            'id': 'search-input'
        })
    )
    
    category = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    
    min_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price',
            'step': '0.01'
        })
    )
    
    max_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price',
            'step': '0.01'
        })
    )
    
    def clean_query(self):
        """
        Sanitize search query
        """
        query = self.cleaned_data.get('query')
        if query:
            query = query.strip()
            # Remove potentially dangerous characters for SQL injection prevention
            # (Django ORM already protects, but this is extra safety)
            if re.search(r'[<>"\';]', query):
                raise ValidationError("Search query contains invalid characters.")
        return query
    
    def clean(self):
        """
        Cross-field validation for price range
        """
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if min_price and max_price and min_price > max_price:
            raise ValidationError("Minimum price cannot be greater than maximum price.")
        
        return cleaned_data

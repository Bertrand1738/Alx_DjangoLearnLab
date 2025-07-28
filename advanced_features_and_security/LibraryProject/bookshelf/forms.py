from django import forms
from .models import Book
from django.core.exceptions import ValidationError
import re

class BookForm(forms.ModelForm):
    """
    Secure form for creating and editing books.
    
    BEGINNER EXPLANATION:
    - ModelForm automatically creates form fields from model
    - We add custom validation to prevent malicious input
    - clean_* methods sanitize and validate specific fields
    - HTML escaping prevents XSS attacks
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': 200,
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': 100,
            }),
            'publication_year': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'YYYY',
                'min': 1000,
                'max': 2100,
            }),
        }

    def clean_title(self):
        """
        Validate and sanitize book title.
        
        Security measures:
        - Strip whitespace
        - Check for minimum length
        - Prevent HTML/script injection
        """
        title = self.cleaned_data.get('title')
        
        if not title:
            raise ValidationError("Title is required.")
        
        # Strip whitespace and convert to title case
        title = title.strip().title()
        
        # Check minimum length
        if len(title) < 2:
            raise ValidationError("Title must be at least 2 characters long.")
        
        # Prevent potential script injection (basic check)
        dangerous_patterns = ['<script', '</script', 'javascript:', 'onclick=', 'onerror=']
        title_lower = title.lower()
        
        for pattern in dangerous_patterns:
            if pattern in title_lower:
                raise ValidationError("Title contains invalid characters.")
        
        return title

    def clean_author(self):
        """
        Validate and sanitize author name.
        
        Security measures:
        - Strip whitespace
        - Check for valid name pattern
        - Prevent injection attacks
        """
        author = self.cleaned_data.get('author')
        
        if not author:
            raise ValidationError("Author is required.")
        
        # Strip whitespace and convert to title case
        author = author.strip().title()
        
        # Check minimum length
        if len(author) < 2:
            raise ValidationError("Author name must be at least 2 characters long.")
        
        # Allow only letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", author):
            raise ValidationError("Author name contains invalid characters. Only letters, spaces, hyphens, and apostrophes are allowed.")
        
        return author

    def clean_publication_year(self):
        """
        Validate publication year.
        
        Security measures:
        - Ensure reasonable year range
        - Prevent negative numbers or extreme values
        """
        year = self.cleaned_data.get('publication_year')
        
        if not year:
            raise ValidationError("Publication year is required.")
        
        # Check reasonable range
        if year < 1000:
            raise ValidationError("Publication year must be 1000 or later.")
        
        if year > 2100:
            raise ValidationError("Publication year cannot be in the far future.")
        
        return year


class BookSearchForm(forms.Form):
    """
    Secure search form for books.
    
    BEGINNER EXPLANATION:
    - Separate form for search functionality
    - Validates search queries to prevent SQL injection
    - Limits search query length to prevent DoS attacks
    """
    
    query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search books by title or author...',
            'maxlength': 100,
        })
    )
    
    search_type = forms.ChoiceField(
        choices=[
            ('all', 'All Fields'),
            ('title', 'Title Only'),
            ('author', 'Author Only'),
        ],
        initial='all',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    def clean_query(self):
        """
        Sanitize search query to prevent injection attacks.
        
        Security measures:
        - Strip whitespace
        - Check for minimum length if provided
        - Remove potentially dangerous characters
        """
        query = self.cleaned_data.get('query')
        
        if query:
            # Strip whitespace
            query = query.strip()
            
            # Minimum length check
            if len(query) < 2:
                raise ValidationError("Search query must be at least 2 characters long.")
            
            # Remove potentially dangerous SQL characters
            dangerous_chars = [';', '--', '/*', '*/', 'xp_', 'sp_']
            query_lower = query.lower()
            
            for char in dangerous_chars:
                if char in query_lower:
                    raise ValidationError("Search query contains invalid characters.")
            
            # Limit special characters
            if query.count('%') > 2 or query.count('_') > 5:
                raise ValidationError("Too many wildcard characters in search.")
        
        return query


class ExampleForm(forms.Form):
    """
    Example form demonstrating Django security best practices.
    
    SECURITY FEATURES DEMONSTRATED:
    - CSRF protection (handled by view)
    - Input validation and sanitization
    - XSS prevention through escaping
    - Field-specific validation methods
    """
    
    name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your name',
            'maxlength': 100,
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email',
        })
    )
    
    message = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your message (optional)',
            'rows': 4,
            'maxlength': 500,
        })
    )
    
    agree_terms = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='I agree to the terms and conditions'
    )

    def clean_name(self):
        """
        Validate and sanitize name field.
        
        Security measures:
        - Strip whitespace
        - Check for minimum length
        - Prevent script injection
        - Allow only safe characters
        """
        name = self.cleaned_data.get('name')
        
        if not name:
            raise ValidationError("Name is required.")
        
        # Strip whitespace and convert to title case
        name = name.strip().title()
        
        # Check minimum length
        if len(name) < 2:
            raise ValidationError("Name must be at least 2 characters long.")
        
        # Prevent potential script injection
        dangerous_patterns = ['<script', '</script', 'javascript:', 'onclick=', 'onerror=']
        name_lower = name.lower()
        
        for pattern in dangerous_patterns:
            if pattern in name_lower:
                raise ValidationError("Name contains invalid characters.")
        
        # Allow only letters, spaces, hyphens, and apostrophes
        if not re.match(r"^[a-zA-Z\s\-'\.]+$", name):
            raise ValidationError("Name can only contain letters, spaces, hyphens, and apostrophes.")
        
        return name

    def clean_message(self):
        """
        Validate and sanitize message field.
        
        Security measures:
        - Strip whitespace
        - Check for reasonable length
        - Prevent script injection
        """
        message = self.cleaned_data.get('message')
        
        if message:
            # Strip whitespace
            message = message.strip()
            
            # Check reasonable length (even though max_length is set)
            if len(message) > 500:
                raise ValidationError("Message is too long (maximum 500 characters).")
            
            # Prevent potential script injection
            dangerous_patterns = ['<script', '</script', 'javascript:', 'onclick=', 'onerror=', 'onload=']
            message_lower = message.lower()
            
            for pattern in dangerous_patterns:
                if pattern in message_lower:
                    raise ValidationError("Message contains invalid content.")
        
        return message

    def clean(self):
        """
        Overall form validation.
        
        Security measures:
        - Cross-field validation
        - Additional security checks
        """
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        email = cleaned_data.get('email')
        
        # Ensure name and email don't match (basic business logic)
        if name and email and name.lower() in email.lower():
            raise ValidationError("Name and email appear to be too similar.")
        
        return cleaned_data

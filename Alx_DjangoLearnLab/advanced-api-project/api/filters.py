"""
Filter classes for API endpoints using django-filter.

FilterSets define how filtering works for each model:
- exact: Exact match (author=1)
- icontains: Case-insensitive partial match (title__icontains="harry")  
- gte/lte: Greater than or equal / Less than or equal (publication_year__gte=2000)
- in: Match any value in a list (author__in=[1,2,3])

URL Examples:
- /api/books/?title__icontains=django  (books with "django" in title)
- /api/books/?publication_year__gte=2000  (books published after 2000)
- /api/books/?author=1  (books by author with ID 1)
- /api/books/?author__name__icontains=rowling  (books by authors with "rowling" in name)
"""

import django_filters
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    """
    Filter class for Book model with comprehensive filtering options.
    
    This class defines all the ways users can filter books:
    - By title (exact match or partial match)
    - By author (by ID or by author name)
    - By publication year (exact, range, or comparison)
    """
    
    # Title filtering
    title = django_filters.CharFilter(
        field_name='title', 
        lookup_expr='icontains',
        help_text='Filter by book title (case-insensitive, partial match)'
    )
    
    # Author filtering (multiple ways)
    author = django_filters.ModelChoiceFilter(
        queryset=Author.objects.all(),
        help_text='Filter by author ID'
    )
    
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains', 
        help_text='Filter by author name (case-insensitive, partial match)'
    )
    
    # Publication year filtering (multiple ways)
    publication_year = django_filters.NumberFilter(
        help_text='Filter by exact publication year'
    )
    
    publication_year_gte = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        help_text='Filter books published on or after this year'
    )
    
    publication_year_lte = django_filters.NumberFilter(
        field_name='publication_year', 
        lookup_expr='lte',
        help_text='Filter books published on or before this year'
    )
    
    # Range filter for publication year
    publication_year_range = django_filters.RangeFilter(
        field_name='publication_year',
        help_text='Filter books within a year range (format: min,max)'
    )
    
    class Meta:
        model = Book
        fields = {
            # Additional fields can be specified here with different lookup options
            # 'title': ['exact', 'icontains', 'startswith'],
            # 'publication_year': ['exact', 'gte', 'lte', 'range'],
        }
    
    def __init__(self, *args, **kwargs):
        """
        Initialize the filter and add custom help text.
        """
        super().__init__(*args, **kwargs)
        
        # You can add custom initialization logic here
        # For example, dynamic filtering based on user permissions

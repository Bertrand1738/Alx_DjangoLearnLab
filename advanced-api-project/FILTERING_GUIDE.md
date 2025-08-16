# Filtering, Searching, and Ordering in Django REST Framework

This guide explains how to use the advanced query capabilities in our Book API.

## Overview

Our API supports three powerful query features:

1. **🔍 Filtering**: Find books that match specific criteria
2. **🔎 Searching**: Text-based search across multiple fields
3. **📊 Ordering**: Sort results by different fields

## Available Endpoints

Both endpoints support the same query capabilities:

- `GET /api/books/` - Simple list view
- `GET /api/books/list-create/` - Combined list/create view

## 1. Filtering (DjangoFilterBackend)

Filtering allows you to narrow down results based on exact criteria.

### Basic Filtering

```
GET /api/books/?publication_year=2020
GET /api/books/?author=1
```

### Text Filtering

```
# Books with "django" in title (case-insensitive)
GET /api/books/?title__icontains=django

# Books by authors with "rowling" in name  
GET /api/books/?author_name__icontains=rowling
```

### Numeric Filtering

```
# Books published in 2000 or later
GET /api/books/?publication_year__gte=2000

# Books published in 2010 or earlier  
GET /api/books/?publication_year__lte=2010

# Books published between 2000-2010
GET /api/books/?publication_year__range=2000,2010
```

### Filter Options Explained

| Filter | Description | Example |
|--------|-------------|---------|
| `exact` | Exact match | `?author=1` |
| `icontains` | Case-insensitive partial match | `?title__icontains=python` |
| `gte` | Greater than or equal | `?publication_year__gte=2000` |
| `lte` | Less than or equal | `?publication_year__lte=2010` |
| `range` | Within range | `?publication_year__range=2000,2010` |

## 2. Searching (SearchFilter)

Searching performs text-based queries across multiple fields simultaneously.

### Basic Search

```
# Search for "harry" in title OR author name
GET /api/books/?search=harry

# Search for "python programming" 
GET /api/books/?search=python programming
```

### Search Fields

The search looks in these fields:
- `title` - Book title
- `author__name` - Author name (related field)

### Search Behavior

- **Case-insensitive**: "HARRY" finds "Harry Potter"
- **Partial matching**: "harr" finds "Harry Potter"  
- **Multiple fields**: Searches title AND author name
- **Multiple words**: "harry potter" finds books with both words

## 3. Ordering (OrderingFilter)

Ordering allows you to sort results by specified fields.

### Basic Ordering

```
# Sort by title A-Z
GET /api/books/?ordering=title

# Sort by title Z-A (descending)
GET /api/books/?ordering=-title

# Sort by publication year (oldest first)
GET /api/books/?ordering=publication_year

# Sort by publication year (newest first)  
GET /api/books/?ordering=-publication_year

# Sort by author name
GET /api/books/?ordering=author__name
```

### Available Ordering Fields

| Field | Description |
|-------|-------------|
| `title` | Book title |
| `publication_year` | Publication year |
| `author__name` | Author name |

Use `-` prefix for descending order (Z-A, newest first).

## 4. Combining Parameters

You can combine filtering, searching, and ordering in a single request:

```
# Search for "python" books, published after 2015, sorted by newest first
GET /api/books/?search=python&publication_year__gte=2015&ordering=-publication_year

# Find books with "django" in title, sorted alphabetically
GET /api/books/?title__icontains=django&ordering=title

# Search + filter + order
GET /api/books/?search=programming&author_name__icontains=smith&ordering=-publication_year
```

## 5. Practical Examples

### Find Programming Books

```bash
# All books with "python" in title
curl "http://localhost:8000/api/books/?title__icontains=python"

# Recent Python books (2020 or newer)
curl "http://localhost:8000/api/books/?title__icontains=python&publication_year__gte=2020"
```

### Find Books by Author

```bash
# Books by J.K. Rowling
curl "http://localhost:8000/api/books/?author_name__icontains=rowling"

# Books by specific author ID
curl "http://localhost:8000/api/books/?author=1"
```

### Browse by Publication Year

```bash
# Classic books (before 2000)
curl "http://localhost:8000/api/books/?publication_year__lte=2000&ordering=publication_year"

# Recent books (2020 or later), newest first
curl "http://localhost:8000/api/books/?publication_year__gte=2020&ordering=-publication_year"
```

### General Search

```bash
# Find anything related to "django"
curl "http://localhost:8000/api/books/?search=django"

# Find "harry potter" books, sorted by publication year
curl "http://localhost:8000/api/books/?search=harry potter&ordering=publication_year"
```

## 6. Using with Frontend Applications

### JavaScript/Ajax Example

```javascript
// Search for Python books
fetch('/api/books/?search=python&ordering=-publication_year')
  .then(response => response.json())
  .then(books => {
    console.log('Found books:', books);
  });

// Filter by year range
fetch('/api/books/?publication_year__range=2000,2020&ordering=title')
  .then(response => response.json())
  .then(books => {
    // Display books published between 2000-2020
  });
```

### Building Dynamic Queries

```javascript
function buildBookQuery(filters) {
  const params = new URLSearchParams();
  
  if (filters.search) params.append('search', filters.search);
  if (filters.author) params.append('author_name__icontains', filters.author);
  if (filters.yearFrom) params.append('publication_year__gte', filters.yearFrom);
  if (filters.yearTo) params.append('publication_year__lte', filters.yearTo);
  if (filters.orderBy) params.append('ordering', filters.orderBy);
  
  return `/api/books/?${params.toString()}`;
}

// Usage
const query = buildBookQuery({
  search: 'programming',
  yearFrom: 2015,
  orderBy: '-publication_year'
});
```

## 7. Error Handling

### Invalid Filters

```json
{
  "detail": "Invalid filter value"
}
```

### Invalid Ordering Fields

If you try to order by a field that's not allowed:

```json
{
  "detail": "Invalid ordering field"
}
```

## 8. Performance Tips

1. **Use specific filters**: `?author=1` is faster than `?search=author name`
2. **Limit results**: Consider pagination for large datasets
3. **Index frequently filtered fields**: Add database indexes for better performance
4. **Combine filters efficiently**: Use filtering before searching when possible

## 9. Testing Your Implementation

Use the provided test script:

```bash
python test_filtering.py
```

Or test manually:

```bash
# Test basic filtering
curl "http://localhost:8000/api/books/?publication_year__gte=2000"

# Test searching  
curl "http://localhost:8000/api/books/?search=python"

# Test ordering
curl "http://localhost:8000/api/books/?ordering=-publication_year"

# Test combination
curl "http://localhost:8000/api/books/?search=book&ordering=title&publication_year__gte=1990"
```

## Summary

Your Book API now supports:

✅ **Filtering** by title, author, and publication year with various lookup types  
✅ **Searching** across title and author name fields  
✅ **Ordering** by title, publication year, and author name  
✅ **Combining** all three capabilities in a single query  
✅ **Flexible querying** for different use cases

This makes your API much more powerful and user-friendly! 🚀

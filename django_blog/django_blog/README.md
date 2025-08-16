# Django API Project

This is a Django REST API project created as part of the ALX Django Learning Lab.

## Project Structure

```
api_project/
├── manage.py
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py          # Contains Book model
│   ├── tests.py
│   ├── views.py
│   └── migrations/
│       ├── __init__.py
│       └── 0001_initial.py
├── api_project/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py        # Django settings with DRF configured
│   ├── urls.py
│   └── wsgi.py
└── .gitignore
```

## Features

- Django 5.2.4
- Django REST Framework configured
- Simple Book model with:
  - Title (CharField, max_length=200)
  - Author (CharField, max_length=100)
  - Created_at (DateTimeField, auto_now_add=True)
  - Updated_at (DateTimeField, auto_now=True)

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/pc-1827/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/api_project
   ```

2. **Install dependencies:**
   ```bash
   pip install django djangorestframework
   ```

3. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the application:**
   Open your browser and go to `http://127.0.0.1:8000/`

## Models

### Book Model
Located in `api/models.py`

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    class Meta:
        ordering = ['title']
```

## Next Steps

- Create serializers for the Book model
- Create API views and viewsets
- Set up URL routing for API endpoints
- Add authentication and permissions
- Create comprehensive tests

## Technology Stack

- **Backend:** Django 5.2.4
- **API Framework:** Django REST Framework
- **Database:** SQLite (default)
- **Python Version:** 3.13+

## License

This project is part of the ALX Django Learning Lab curriculum.

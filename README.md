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

# Django Blog Project

## Overview
This project is a Django-based blog application with user authentication and full blog post management (CRUD) features.

## Features
- **User Authentication:** Registration, login, logout, and profile management.
- **Blog Post Management:** Create, read, update, and delete posts.
- **Permissions:** Only authenticated users can create posts; only authors can edit or delete their own posts.
- **Security:** CSRF protection and password hashing are enabled by default.
- **Automated Tests:** All major features are covered by tests.

## Directory Structure
```
django_blog/
├── blog/
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   ├── templates/
│   │   └── blog/
│   │       ├── login.html
│   │       ├── logout.html
│   │       ├── profile.html
│   │       ├── register.html
│   │       ├── post_list.html
│   │       ├── post_detail.html
│   │       ├── post_form.html
│   │       └── post_confirm_delete.html
│   └── static/
│       └── css/
│           └── style.css
├── django_blog/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── __init__.py
├── manage.py
└── README.md
```

## Usage
1. **Install dependencies:**
   ```bash
   pip install django
   ```
2. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
3. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```
4. **Run the server:**
   ```bash
   python manage.py runserver
   ```
5. **Access the app:**
   - Home: `/posts/`
   - Register: `/register/`
   - Login: `/login/`
   - Profile: `/profile/`

## Testing
Run all tests with:
```bash
python manage.py test blog
```

## Notes
- Only logged-in users can create, edit, or delete posts.
- Authors can only edit or delete their own posts.
- All templates use the provided CSS for styling.
- CSRF protection is enabled in all forms.

## Author
- [Your Name]

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

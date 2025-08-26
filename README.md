<<<<<<< HEAD
# Social Media API

## Overview
A Django REST Framework-based API for user authentication and profile management. Features a custom user model with bio, profile picture, and followers.

## Setup Instructions

1. **Clone the repository**
2. **Install dependencies**
   - Python 3.10+
   - Django 5.2+
   - Django REST Framework
   - Pillow (for image uploads)
   - Install with:
     ```bash
     pip install django djangorestframework pillow
     ```
3. **Apply migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Run the development server**
=======
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
>>>>>>> abacb1d76f0775afded1fee1488f7046a94344ed
   ```bash
   python manage.py runserver
   ```

<<<<<<< HEAD
## User Model
- Extends Django's `AbstractUser`
- Fields: `bio`, `profile_picture`, `followers` (ManyToMany)

## API Endpoints

### Registration
- **POST** `/api/accounts/register/`
- Request: `{ "username": "user", "email": "email", "password": "pass", "bio": "...", "profile_picture": <file> }`
- Response: `{ "user": {...}, "token": "..." }`

### Login
- **POST** `/api/accounts/login/`
- Request: `{ "username": "user", "password": "pass" }`
- Response: `{ "user": {...}, "token": "..." }`

### Profile
- **GET/PUT** `/api/accounts/profile/`
- Auth required (Token in `Authorization: Token <token>` header)
- View or update profile

## Testing
Use Postman or similar tools to test registration, login, and profile endpoints. Ensure tokens are returned and authentication works.

## Project Structure
- `accounts/models.py`: Custom user model
- `accounts/serializers.py`: DRF serializers
- `accounts/views.py`: API views
- `accounts/urls.py`: Endpoint routing
- `social_media_api/settings.py`: Project settings
- `social_media_api/urls.py`: Main URL config

---
For questions or issues, contact the maintainer.
=======
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
>>>>>>> abacb1d76f0775afded1fee1488f7046a94344ed

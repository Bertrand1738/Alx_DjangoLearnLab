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
   ```bash
   python manage.py runserver
   ```

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

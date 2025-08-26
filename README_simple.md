# Social Media API

A Django REST Framework-based API for social media features including user authentication, posts, and comments.

## Setup

1. Install dependencies: `pip install django djangorestframework pillow django-filter`
2. Apply migrations: `python manage.py migrate`
3. Run server: `python manage.py runserver`

## Features

- User authentication with custom user model (bio, profile picture, followers)
- Posts and comments CRUD operations
- Pagination, filtering, and search

## API Endpoints

- `/api/accounts/register/`, `/api/accounts/login/`, `/api/accounts/profile/`
- `/api/posts/`, `/api/posts/{id}/`
- `/api/comments/`, `/api/comments/{id}/`

All endpoints documented in `posts/API_DOCUMENTATION.md`

## Authentication

Use token auth: `Authorization: Token <token>`

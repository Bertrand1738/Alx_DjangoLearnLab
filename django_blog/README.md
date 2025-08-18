# Django Blog - Post Management

This project implements a blog system with full CRUD operations.

## Features
- List all posts (`/`)
- View single post (`/posts/<id>/`)
- Create new post (`/posts/new/`) – login required
- Edit post (`/posts/<id>/edit/`) – only author
- Delete post (`/posts/<id>/delete/`) – only author
- User registration, login, logout, and profile management

## Permissions
- Anyone can view list & detail pages
- Only logged-in users can create posts
- Only authors can edit or delete their own posts

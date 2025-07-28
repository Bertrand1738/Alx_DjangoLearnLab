# Django Permissions and Groups Documentation

## 🎯 Overview

This Django application demonstrates a comprehensive permissions and groups system for controlling access to different parts of the application. Users are assigned to groups, and groups have specific permissions that determine what actions users can perform.

## 🔐 Permission System

### Custom Permissions

We've defined custom permissions for the Book model:

- **can_view**: Allows viewing books in the library
- **can_create**: Allows creating new books
- **can_edit**: Allows editing existing books
- **can_delete**: Allows deleting books

### User Groups

Three groups are configured with different permission levels:

#### 👁️ Viewers Group
- **Permissions**: can_view
- **Can do**: View books only
- **Cannot do**: Create, edit, or delete books
- **Use case**: Read-only access for general users

#### ✏️ Editors Group
- **Permissions**: can_view, can_create, can_edit
- **Can do**: View, create, and edit books
- **Cannot do**: Delete books
- **Use case**: Content managers who maintain the library

#### 👑 Admins Group
- **Permissions**: can_view, can_create, can_edit, can_delete
- **Can do**: Everything with books
- **Use case**: Full administrative access

## 🚀 Quick Start

### 1. Set Up Permissions and Groups
```bash
python manage.py setup_permissions
```

### 2. Create Test Users
```bash
python manage.py create_test_users
```

### 3. Create Sample Books
```bash
python manage.py create_sample_books
```

### 4. Start the Server
```bash
python manage.py runserver
```

## 🧪 Testing the System

### Test Credentials

| Username | Password | Group | Permissions |
|----------|----------|-------|-------------|
| viewer_user | testpass123 | Viewers | View only |
| editor_user | testpass123 | Editors | View, Create, Edit |
| admin_user | testpass123 | Admins | All permissions |

### Testing URLs

- **Book List**: http://127.0.0.1:8000/bookshelf/books/
- **Permission Check**: http://127.0.0.1:8000/bookshelf/permissions/
- **Django Admin**: http://127.0.0.1:8000/admin/

### Testing Steps

1. **Log in as viewer_user**:
   - ✅ Can see the book list
   - ❌ Cannot see "Add New Book" button
   - ❌ Cannot see Edit/Delete buttons on books

2. **Log in as editor_user**:
   - ✅ Can see the book list
   - ✅ Can create new books
   - ✅ Can edit existing books
   - ❌ Cannot delete books

3. **Log in as admin_user**:
   - ✅ Can do everything
   - ✅ Can delete books

## 🔧 Implementation Details

### Models (models.py)

```python
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    class Meta:
        permissions = [
            ('can_view', 'Can view book'),
            ('can_create', 'Can create book'),
            ('can_edit', 'Can edit book'),
            ('can_delete', 'Can delete book'),
        ]
```

### Views (views.py)

Each view is protected with decorators:

```python
@login_required
@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    # View implementation
```

### Templates

Templates check permissions before showing UI elements:

```html
{% if user.has_perm:'bookshelf.can_create' %}
    <a href="{% url 'book_create' %}">Add New Book</a>
{% endif %}
```

## 🛡️ Security Features

1. **Login Required**: All views require authentication
2. **Permission Checking**: Views check specific permissions
3. **Template Guards**: UI elements only show if user has permission
4. **Graceful Degradation**: Users see appropriate messages when lacking permissions
5. **Exception Handling**: 403 errors for unauthorized access

## 🔄 Adding New Permissions

To add new permissions:

1. **Add to model Meta**:
```python
class Meta:
    permissions = [
        ('new_permission', 'Description of permission'),
    ]
```

2. **Create migration**:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Update views**:
```python
@permission_required('app.new_permission', raise_exception=True)
def new_view(request):
    # Implementation
```

4. **Update templates**:
```html
{% if user.has_perm:'app.new_permission' %}
    <!-- Show protected content -->
{% endif %}
```

## 🔍 Troubleshooting

### Common Issues

1. **Permission Denied (403 Error)**:
   - Check if user is in correct group
   - Verify group has required permissions
   - Check if user is logged in

2. **Groups Not Showing**:
   - Run `python manage.py setup_permissions`
   - Check Django admin for group configuration

3. **Users Can't Access Anything**:
   - Assign users to appropriate groups
   - Verify groups have permissions assigned

### Debugging Commands

```bash
# Check user permissions
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.get(username='viewer_user')
print('Groups:', user.groups.all())
print('Permissions:', user.get_all_permissions())
"
```

## 📚 Further Reading

- [Django Permissions Documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#permissions-and-authorization)
- [Django Groups Documentation](https://docs.djangoproject.com/en/stable/topics/auth/default/#groups)
- [Permission Decorators](https://docs.djangoproject.com/en/stable/topics/auth/default/#the-permission-required-decorator)

---

## 🎉 Success!

You now have a fully functional permissions and groups system in Django! This provides the foundation for building secure, role-based applications.

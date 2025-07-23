"""
Custom Permissions Management Script

BEGINNER EXPLANATION:
This script demonstrates how to assign custom permissions to users in Django.
Run this script to set up sample users with different permission levels.

USAGE:
python manage.py shell < setup_permissions.py
"""

from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from relationship_app.models import Book, UserProfile

def setup_permissions():
    """Set up sample users with different permission levels for testing."""
    
    print("=== SETTING UP CUSTOM PERMISSIONS DEMO ===\n")
    
    # Get or create content type for Book model
    book_content_type = ContentType.objects.get_for_model(Book)
    
    # Get our custom permissions
    try:
        add_book_perm = Permission.objects.get(
            codename='can_add_book',
            content_type=book_content_type
        )
        change_book_perm = Permission.objects.get(
            codename='can_change_book',
            content_type=book_content_type
        )
        delete_book_perm = Permission.objects.get(
            codename='can_delete_book',
            content_type=book_content_type
        )
        print("✓ Custom permissions found in database")
    except Permission.DoesNotExist:
        print("✗ Custom permissions not found! Make sure migrations are applied.")
        return
    
    # Create groups with different permission levels
    # 1. Book Editors - Can add and edit books
    editors_group, created = Group.objects.get_or_create(name='Book Editors')
    if created:
        editors_group.permissions.add(add_book_perm, change_book_perm)
        print("✓ Created 'Book Editors' group with add and change permissions")
    else:
        print("- 'Book Editors' group already exists")
    
    # 2. Book Managers - Can add, edit, and delete books
    managers_group, created = Group.objects.get_or_create(name='Book Managers')
    if created:
        managers_group.permissions.add(add_book_perm, change_book_perm, delete_book_perm)
        print("✓ Created 'Book Managers' group with full permissions")
    else:
        print("- 'Book Managers' group already exists")
    
    # Create sample users for testing
    users_to_create = [
        {
            'username': 'book_viewer',
            'password': 'testpass123',
            'role': 'Member',
            'permissions': [],  # No book permissions
            'description': 'Can only view books'
        },
        {
            'username': 'book_editor',
            'password': 'testpass123',
            'role': 'Librarian',
            'permissions': [add_book_perm, change_book_perm],
            'description': 'Can add and edit books'
        },
        {
            'username': 'book_manager',
            'password': 'testpass123',
            'role': 'Admin',
            'permissions': [add_book_perm, change_book_perm, delete_book_perm],
            'description': 'Can add, edit, and delete books'
        },
    ]
    
    print("\n=== CREATING TEST USERS ===")
    for user_data in users_to_create:
        username = user_data['username']
        
        # Create user if doesn't exist
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'password': user_data['password'],
                'email': f"{username}@example.com"
            }
        )
        
        if created:
            user.set_password(user_data['password'])
            user.save()
            print(f"✓ Created user: {username}")
        else:
            print(f"- User already exists: {username}")
        
        # Create or update UserProfile
        profile, profile_created = UserProfile.objects.get_or_create(
            user=user,
            defaults={'role': user_data['role']}
        )
        
        if profile_created:
            print(f"  ✓ Created profile with role: {user_data['role']}")
        else:
            profile.role = user_data['role']
            profile.save()
            print(f"  - Updated profile role to: {user_data['role']}")
        
        # Assign permissions
        user.user_permissions.clear()  # Clear existing permissions
        for permission in user_data['permissions']:
            user.user_permissions.add(permission)
        
        if user_data['permissions']:
            perm_names = [p.codename for p in user_data['permissions']]
            print(f"  ✓ Assigned permissions: {', '.join(perm_names)}")
        else:
            print(f"  - No book permissions assigned")
    
    print("\n=== PERMISSION ASSIGNMENT SUMMARY ===")
    for user_data in users_to_create:
        user = User.objects.get(username=user_data['username'])
        print(f"\n{user.username} ({user_data['description']}):")
        print(f"  - Role: {user.userprofile.role}")
        print(f"  - Can add books: {user.has_perm('relationship_app.can_add_book')}")
        print(f"  - Can change books: {user.has_perm('relationship_app.can_change_book')}")
        print(f"  - Can delete books: {user.has_perm('relationship_app.can_delete_book')}")
    
    print("\n=== TESTING INSTRUCTIONS ===")
    print("1. Run the Django development server:")
    print("   python manage.py runserver")
    print("\n2. Test the permission system by logging in as different users:")
    print("   - book_viewer / testpass123 (can only view)")
    print("   - book_editor / testpass123 (can add and edit)")
    print("   - book_manager / testpass123 (can add, edit, and delete)")
    print("\n3. Visit these URLs to test permissions:")
    print("   - /relationship_app/books_with_permissions/ (main test page)")
    print("   - /relationship_app/add_book/ (test add permission)")
    print("   - /relationship_app/edit_book/1/ (test edit permission)")
    print("   - /relationship_app/delete_book/1/ (test delete permission)")
    
    print("\n=== SETUP COMPLETE ===")

# Run the setup
if __name__ == '__main__':
    setup_permissions()
else:
    # When run via 'python manage.py shell < script.py'
    setup_permissions()

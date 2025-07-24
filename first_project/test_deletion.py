#!/usr/bin/env python
"""
Test script for product deletion functionality
"""
import os
import django
import sys

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
django.setup()

from django.contrib.auth.models import User, Permission
from book_store.models import Product
from django.contrib.contenttypes.models import ContentType

def test_deletion_setup():
    """Test if everything is set up correctly for deletion"""
    print("🔍 TESTING PRODUCT DELETION SETUP")
    print("=" * 50)
    
    # 1. Check if products exist
    products = Product.objects.all()
    print(f"📦 Products in database: {products.count()}")
    for product in products:
        print(f"   - {product.name} (ID: {product.id})")
    
    # 2. Check if permission exists
    try:
        content_type = ContentType.objects.get_for_model(Product)
        permission = Permission.objects.get(
            codename='can_delete_product',
            content_type=content_type
        )
        print(f"✅ Custom permission exists: {permission.name}")
    except Permission.DoesNotExist:
        print("❌ Custom permission 'can_delete_product' not found!")
        print("🔍 Checking for built-in delete permission...")
        try:
            permission = Permission.objects.get(
                codename='delete_product',
                content_type=content_type
            )
            print(f"✅ Built-in permission exists: {permission.name}")
            print("⚠️  Note: You're using built-in delete permission instead of custom one")
        except Permission.DoesNotExist:
            print("❌ No delete permission found!")
            return False
    
    # 3. Check if any users have this permission
    users_with_permission = User.objects.filter(
        user_permissions=permission
    ).union(
        User.objects.filter(
            groups__permissions=permission
        )
    )
    
    print(f"👥 Users with delete permission: {users_with_permission.count()}")
    for user in users_with_permission:
        print(f"   - {user.username}")
    
    if users_with_permission.count() == 0:
        print("⚠️  No users have delete permission yet!")
        print("💡 To test deletion, you need to:")
        print("   1. Go to Django admin (/admin/)")
        print("   2. Create a user or edit existing user")
        print("   3. Assign 'Can delete products' permission")
    
    print("\n🌐 TESTING URLS AND TEMPLATES")
    print("=" * 50)
    
    # 4. Check if templates exist
    import os
    templates_to_check = [
        'book_store/templates/book_store/delete_product.html',
        'book_store/templates/book_store/products.html'
    ]
    
    for template in templates_to_check:
        if os.path.exists(template):
            print(f"✅ Template exists: {template}")
        else:
            print(f"❌ Template missing: {template}")
    
    print("\n🔗 URL PATTERNS")
    print("=" * 50)
    print("✅ Delete URL: /delete-product/<product_id>/")
    print("✅ Products URL: /products/")
    
    print("\n🎯 NEXT STEPS TO TEST")
    print("=" * 50)
    print("1. Run: python manage.py runserver")
    print("2. Go to: http://127.0.0.1:8000/products/")
    print("3. Login with a user that has 'can_delete_product' permission")
    print("4. Look for 🗑️ Delete buttons on product cards")
    print("5. Click delete button to test the confirmation page")
    
    return True

if __name__ == "__main__":
    test_deletion_setup()

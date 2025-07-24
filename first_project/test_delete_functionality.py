#!/usr/bin/env python
"""
Test the delete product functionality directly
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
django.setup()

from book_store.models import Product
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

def test_delete_functionality():
    print("🧪 TESTING DELETE FUNCTIONALITY")
    print("=" * 50)
    
    # Check current products
    products_before = Product.objects.count()
    print(f"📦 Products before test: {products_before}")
    
    if products_before == 0:
        print("❌ No products to test with!")
        return
    
    # Get first product
    test_product = Product.objects.first()
    print(f"🎯 Testing with product: {test_product.name} (ID: {test_product.id})")
    
    # Test URL generation
    delete_url = reverse('delete_product', args=[test_product.id])
    print(f"🔗 Delete URL: {delete_url}")
    
    # Create test client
    client = Client()
    
    # Get superuser
    try:
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            print(f"👤 Testing with superuser: {superuser.username}")
            client.force_login(superuser)
        else:
            print("❌ No superuser found!")
            return
    except Exception as e:
        print(f"❌ Error getting superuser: {e}")
        return
    
    # Test GET request (should show confirmation page)
    print("\n🔍 Testing GET request to delete page...")
    try:
        response = client.get(delete_url)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Delete confirmation page loads successfully")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            return
    except Exception as e:
        print(f"   ❌ Error accessing delete page: {e}")
        return
    
    # Test POST request (should actually delete)
    print("\n🗑️ Testing POST request to delete product...")
    try:
        response = client.post(delete_url)
        print(f"   Status Code: {response.status_code}")
        
        # Check if product was deleted
        products_after = Product.objects.count()
        print(f"   Products after deletion: {products_after}")
        
        if products_after == products_before - 1:
            print("   ✅ Product deleted successfully!")
        else:
            print("   ❌ Product was not deleted")
            
        # Check if redirected
        if response.status_code == 302:
            print(f"   ✅ Redirected to: {response.url}")
        else:
            print(f"   ⚠️ Expected redirect, got: {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Error during POST request: {e}")

if __name__ == "__main__":
    test_delete_functionality()

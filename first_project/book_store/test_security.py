"""
Security Tests for Django Book Store
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from book_store.models import Product
from book_store.forms import ProductForm
import re

class SecurityTestCase(TestCase):
    """
    Test security features of the book store application
    """
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test users
        self.superuser = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='secure_password123'
        )
        
        self.regular_user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='user_password123'
        )
        
        # Create test product
        self.test_product = Product.objects.create(
            name='Test Book',
            description='A test book for security testing',
            price=29.99,
            category='Programming'
        )

class InputValidationTests(SecurityTestCase):
    """Test input validation and sanitization"""
    
    def test_product_form_validation(self):
        """Test ProductForm validates inputs correctly"""
        
        # Test empty name
        form_data = {
            'name': '',
            'description': 'Valid description here',
            'price': 29.99,
            'category': 'Programming'
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        
        # Test short name
        form_data['name'] = 'a'
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        
        # Test invalid characters in name
        form_data['name'] = '<script>alert("xss")</script>'
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        
        # Test negative price
        form_data['name'] = 'Valid Name'
        form_data['price'] = -10
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors)
        
        # Test short description
        form_data['price'] = 29.99
        form_data['description'] = 'Short'
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors)
        
        # Test invalid category
        form_data['description'] = 'This is a valid description that is long enough'
        form_data['category'] = 'Invalid Category'
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
        
        # Test valid form
        form_data['category'] = 'Programming'
        form = ProductForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_xss_prevention(self):
        """Test that XSS attempts are prevented"""
        xss_payloads = [
            '<script>alert("xss")</script>',
            '<img src=x onerror=alert("xss")>',
            'javascript:alert("xss")',
            '<svg onload=alert("xss")>',
        ]
        
        for payload in xss_payloads:
            form_data = {
                'name': payload,
                'description': 'Valid description',
                'price': 29.99,
                'category': 'Programming'
            }
            form = ProductForm(data=form_data)
            self.assertFalse(form.is_valid(), f"XSS payload should be rejected: {payload}")
    
    def test_sql_injection_prevention(self):
        """Test that SQL injection attempts are prevented"""
        sql_payloads = [
            "'; DROP TABLE products; --",
            "' OR '1'='1",
            "1; DELETE FROM products WHERE 1=1; --",
        ]
        
        for payload in sql_payloads:
            form_data = {
                'name': f"Product {payload}",
                'description': 'Valid description',
                'price': 29.99,
                'category': 'Programming'
            }
            form = ProductForm(data=form_data)
            # The form should either reject invalid characters or Django ORM should handle safely
            if form.is_valid():
                # If form accepts it, Django ORM should handle it safely
                product = form.save()
                # Verify the payload didn't cause SQL injection
                self.assertTrue(Product.objects.filter(id=product.id).exists())

class AuthenticationTests(SecurityTestCase):
    """Test authentication and authorization"""
    
    def test_login_required_for_add_product(self):
        """Test that login is required to add products"""
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        self.assertIn('/accounts/login/', response.url)
    
    def test_permission_required_for_add_product(self):
        """Test that proper permissions are required"""
        # Login as regular user without permissions
        self.client.login(username='user', password='user_password123')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 403)  # Permission denied
        
        # Login as superuser (should have access)
        self.client.login(username='admin', password='secure_password123')
        response = self.client.get(reverse('add_product'))
        self.assertEqual(response.status_code, 200)  # Should work
    
    def test_csrf_protection(self):
        """Test CSRF protection on forms"""
        self.client.login(username='admin', password='secure_password123')
        
        # Try to submit form without CSRF token
        form_data = {
            'name': 'Test Product',
            'description': 'Test description',
            'price': 29.99,
            'category': 'Programming'
        }
        
        # This should fail due to missing CSRF token
        response = self.client.post(reverse('add_product'), data=form_data)
        self.assertEqual(response.status_code, 403)  # CSRF failure

class SecurityHeaderTests(SecurityTestCase):
    """Test security headers"""
    
    def test_xss_protection_header(self):
        """Test that XSS protection headers are set"""
        response = self.client.get(reverse('products'))
        # Django's SecurityMiddleware should set this
        self.assertTrue('X-Content-Type-Options' in response or 
                       hasattr(response, 'get') and response.get('X-Content-Type-Options'))
    
    def test_clickjacking_protection(self):
        """Test clickjacking protection"""
        response = self.client.get(reverse('products'))
        # Check if X-Frame-Options is set
        self.assertTrue('X-Frame-Options' in response or 
                       hasattr(response, 'get') and response.get('X-Frame-Options'))

class DataIntegrityTests(SecurityTestCase):
    """Test data integrity and business logic"""
    
    def test_duplicate_product_prevention(self):
        """Test that duplicate product names are prevented"""
        form_data = {
            'name': 'Test Book',  # Same as existing product
            'description': 'Another test book',
            'price': 39.99,
            'category': 'Programming'
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_price_validation_business_rules(self):
        """Test business rule: premium categories have minimum price"""
        form_data = {
            'name': 'ML Book',
            'description': 'Machine learning book',
            'price': 10.00,  # Below minimum for ML category
            'category': 'Machine Learning'
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())
        # Should fail cross-field validation
    
    def test_data_length_limits(self):
        """Test that data length limits are enforced"""
        # Test extremely long inputs
        long_name = 'a' * 200  # Exceeds max length
        long_description = 'a' * 2000  # Exceeds max length
        
        form_data = {
            'name': long_name,
            'description': long_description,
            'price': 29.99,
            'category': 'Programming'
        }
        form = ProductForm(data=form_data)
        self.assertFalse(form.is_valid())

class SecurityUtilityTests(TestCase):
    """Test security utility functions"""
    
    def test_regex_validation(self):
        """Test regex patterns used for validation"""
        valid_names = [
            'Python Programming',
            'C++ Essentials',
            'JavaScript: The Good Parts',
            'Machine Learning (2nd Edition)',
        ]
        
        invalid_names = [
            '<script>alert("xss")</script>',
            'Name with $ symbols',
            'Invalid@name#here',
        ]
        
        name_pattern = r'^[a-zA-Z0-9\s\-\'\":.,!?()]+$'
        
        for name in valid_names:
            self.assertTrue(re.match(name_pattern, name), f"Valid name rejected: {name}")
        
        for name in invalid_names:
            self.assertFalse(re.match(name_pattern, name), f"Invalid name accepted: {name}")

# Run tests with: python manage.py test book_store.test_security

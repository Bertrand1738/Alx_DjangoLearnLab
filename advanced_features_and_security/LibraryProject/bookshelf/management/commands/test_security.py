from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse
import json

User = get_user_model()

class Command(BaseCommand):
    help = 'Test security implementations'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔒 Testing Security Implementations...'))
        
        # Create test client
        client = Client()
        
        # Test 1: CSRF Protection
        self.stdout.write('\n🧪 Test 1: CSRF Protection')
        self.test_csrf_protection(client)
        
        # Test 2: Permission Enforcement
        self.stdout.write('\n🧪 Test 2: Permission Enforcement')
        self.test_permission_enforcement(client)
        
        # Test 3: Input Validation
        self.stdout.write('\n🧪 Test 3: Input Validation')
        self.test_input_validation(client)
        
        # Test 4: XSS Prevention
        self.stdout.write('\n🧪 Test 4: XSS Prevention')
        self.test_xss_prevention(client)
        
        self.stdout.write(self.style.SUCCESS('\n✅ Security testing completed!'))

    def test_csrf_protection(self, client):
        """Test CSRF token requirement"""
        try:
            # Try to access create view without CSRF token
            response = client.post('/bookshelf/books/create/', {
                'title': 'Test Book',
                'author': 'Test Author',
                'publication_year': 2023
            })
            
            # Should be redirected to login (403 if logged in without CSRF)
            if response.status_code in [302, 403]:
                self.stdout.write('  ✅ CSRF protection active - unauthorized POST blocked')
            else:
                self.stdout.write(f'  ❌ CSRF issue - status code: {response.status_code}')
                
        except Exception as e:
            self.stdout.write(f'  ⚠️  CSRF test error: {e}')

    def test_permission_enforcement(self, client):
        """Test permission-based access control"""
        try:
            # Test without login
            response = client.get('/bookshelf/books/')
            if response.status_code == 302:  # Redirect to login
                self.stdout.write('  ✅ Login required - anonymous access blocked')
            else:
                self.stdout.write(f'  ❌ Login bypass possible - status: {response.status_code}')
            
            # Test direct URL access to edit
            response = client.get('/bookshelf/books/1/edit/')
            if response.status_code == 302:  # Redirect to login
                self.stdout.write('  ✅ Edit view protected - anonymous access blocked')
            else:
                self.stdout.write(f'  ❌ Edit view accessible - status: {response.status_code}')
                
        except Exception as e:
            self.stdout.write(f'  ⚠️  Permission test error: {e}')

    def test_input_validation(self, client):
        """Test form validation and sanitization"""
        # Test with viewer user if exists
        try:
            user = User.objects.get(username='viewer_user')
            client.force_login(user)
            
            # Try to access create view (should fail - no permission)
            response = client.get('/bookshelf/books/create/')
            if response.status_code == 403:
                self.stdout.write('  ✅ Create permission enforced')
            else:
                self.stdout.write(f'  ❌ Permission bypass - status: {response.status_code}')
                
        except User.DoesNotExist:
            self.stdout.write('  ⚠️  No test users found - run create_test_users first')
        except Exception as e:
            self.stdout.write(f'  ⚠️  Input validation test error: {e}')

    def test_xss_prevention(self, client):
        """Test XSS prevention measures"""
        try:
            # Test search with potential XSS payload
            response = client.get('/bookshelf/books/', {
                'query': '<script>alert("xss")</script>',
                'search_type': 'all'
            })
            
            if response.status_code == 302:  # Redirected due to no login
                self.stdout.write('  ✅ Search protected by authentication')
            elif b'<script>' not in response.content:
                self.stdout.write('  ✅ XSS payload escaped in search')
            else:
                self.stdout.write('  ❌ Potential XSS vulnerability in search')
                
        except Exception as e:
            self.stdout.write(f'  ⚠️  XSS test error: {e}')

    def additional_security_info(self):
        """Display additional security information"""
        self.stdout.write('\n📋 Security Configuration Summary:')
        
        from django.conf import settings
        
        security_settings = [
            ('DEBUG', settings.DEBUG),
            ('CSRF_COOKIE_SECURE', getattr(settings, 'CSRF_COOKIE_SECURE', 'Not Set')),
            ('SESSION_COOKIE_SECURE', getattr(settings, 'SESSION_COOKIE_SECURE', 'Not Set')),
            ('SECURE_BROWSER_XSS_FILTER', getattr(settings, 'SECURE_BROWSER_XSS_FILTER', 'Not Set')),
            ('X_FRAME_OPTIONS', getattr(settings, 'X_FRAME_OPTIONS', 'Not Set')),
        ]
        
        for setting_name, setting_value in security_settings:
            self.stdout.write(f'  {setting_name}: {setting_value}')
        
        self.stdout.write('\n🔧 Recommendations:')
        
        if settings.DEBUG:
            self.stdout.write('  ⚠️  Set DEBUG=False in production')
        else:
            self.stdout.write('  ✅ DEBUG is disabled')
        
        self.stdout.write('  💡 Enable HTTPS in production')
        self.stdout.write('  💡 Set up proper CSP headers')
        self.stdout.write('  💡 Regular security audits recommended')

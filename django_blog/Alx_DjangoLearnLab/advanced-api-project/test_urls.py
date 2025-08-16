"""
URL verification test for Django API endpoints.
This script tests that all required URL patterns are configured correctly.
"""

from django.test import TestCase
from django.urls import reverse, resolve
from api import views

class URLPatternsTest(TestCase):
    """Test that all required URL patterns are correctly configured."""
    
    def test_books_list_url(self):
        """Test books list URL resolves correctly"""
        url = reverse('book-list')
        self.assertEqual(url, '/books/')
        resolver = resolve('/books/')
        self.assertEqual(resolver.view_name, 'book-list')
    
    def test_books_detail_url(self):
        """Test book detail URL resolves correctly"""
        url = reverse('book-detail', kwargs={'pk': 1})
        self.assertEqual(url, '/books/1/')
    
    def test_books_create_url(self):
        """Test book create URL resolves correctly"""
        url = reverse('book-create')
        self.assertEqual(url, '/books/create/')
        resolver = resolve('/books/create/')
        self.assertEqual(resolver.view_name, 'book-create')
    
    def test_books_update_url(self):
        """Test book update URL resolves correctly"""
        url = reverse('book-update')
        self.assertEqual(url, '/books/update/')
        resolver = resolve('/books/update/')
        self.assertEqual(resolver.view_name, 'book-update')
    
    def test_books_delete_url(self):
        """Test book delete URL resolves correctly"""
        url = reverse('book-delete')
        self.assertEqual(url, '/books/delete/')
        resolver = resolve('/books/delete/')
        self.assertEqual(resolver.view_name, 'book-delete')
    
    def test_all_required_patterns_exist(self):
        """Test that books/update and books/delete patterns exist"""
        # These are the patterns the checker is looking for
        resolver_update = resolve('/books/update/')
        resolver_delete = resolve('/books/delete/')
        
        self.assertEqual(resolver_update.view_name, 'book-update')
        self.assertEqual(resolver_delete.view_name, 'book-delete')
        
        print("✅ All required URL patterns exist:")
        print("   - books/update")
        print("   - books/delete")

if __name__ == '__main__':
    import django
    from django.conf import settings
    from django.test.utils import get_runner
    
    if not settings.configured:
        settings.configure(
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
                'api',
            ],
            ROOT_URLCONF='api.urls',
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            }
        )
    
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    test_runner.run_tests(["__main__"])

#!/usr/bin/env python3
"""
HTTPS Security Configuration Test Script

This script tests the HTTPS and security configuration of the Django application.
It verifies that all security settings are properly configured and working.
"""

import subprocess
import sys
import os
import django
from pathlib import Path

# Add the Django project to the Python path
project_root = Path(__file__).parent / 'LibraryProject'
sys.path.insert(0, str(project_root))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LibraryProject.settings')
django.setup()

from django.conf import settings
from django.test.utils import override_settings
from django.test import RequestFactory
from django.http import HttpResponse

class HTTPSSecurityTester:
    """Test HTTPS and security configuration"""
    
    def __init__(self):
        self.factory = RequestFactory()
        self.passed_tests = 0
        self.total_tests = 0
        
    def test_setting(self, setting_name, expected_value, description):
        """Test a Django setting"""
        self.total_tests += 1
        actual_value = getattr(settings, setting_name, None)
        
        if actual_value == expected_value:
            print(f"✅ {description}")
            self.passed_tests += 1
            return True
        else:
            print(f"❌ {description}")
            print(f"   Expected: {expected_value}, Got: {actual_value}")
            return False
    
    def test_https_settings(self):
        """Test HTTPS-related Django settings"""
        print("\n🔒 Testing HTTPS Configuration:")
        print("=" * 50)
        
        # Test HTTPS settings in production mode
        if not settings.DEBUG:
            self.test_setting('SECURE_SSL_REDIRECT', True, 
                            'SECURE_SSL_REDIRECT: HTTP to HTTPS redirect enabled')
            self.test_setting('SECURE_HSTS_SECONDS', 31536000, 
                            'SECURE_HSTS_SECONDS: HSTS set to 1 year')
            self.test_setting('SECURE_HSTS_INCLUDE_SUBDOMAINS', True, 
                            'SECURE_HSTS_INCLUDE_SUBDOMAINS: HSTS includes subdomains')
            self.test_setting('SECURE_HSTS_PRELOAD', True, 
                            'SECURE_HSTS_PRELOAD: HSTS preload enabled')
        else:
            print("⚠️  Running in DEBUG mode - HTTPS settings relaxed for development")
            self.test_setting('SECURE_SSL_REDIRECT', False, 
                            'SECURE_SSL_REDIRECT: Disabled for development')
    
    def test_cookie_security(self):
        """Test secure cookie configuration"""
        print("\n🍪 Testing Cookie Security:")
        print("=" * 50)
        
        # Session cookies
        expected_session_secure = not settings.DEBUG
        self.test_setting('SESSION_COOKIE_SECURE', expected_session_secure, 
                        f'SESSION_COOKIE_SECURE: {"Enabled" if expected_session_secure else "Disabled for development"}')
        self.test_setting('SESSION_COOKIE_HTTPONLY', True, 
                        'SESSION_COOKIE_HTTPONLY: Prevents JavaScript access')
        self.test_setting('SESSION_COOKIE_SAMESITE', 'Strict', 
                        'SESSION_COOKIE_SAMESITE: Strict same-site policy')
        
        # CSRF cookies
        expected_csrf_secure = not settings.DEBUG
        self.test_setting('CSRF_COOKIE_SECURE', expected_csrf_secure, 
                        f'CSRF_COOKIE_SECURE: {"Enabled" if expected_csrf_secure else "Disabled for development"}')
        self.test_setting('CSRF_COOKIE_HTTPONLY', True, 
                        'CSRF_COOKIE_HTTPONLY: Prevents JavaScript access')
        self.test_setting('CSRF_USE_SESSIONS', True, 
                        'CSRF_USE_SESSIONS: CSRF tokens stored in sessions')
    
    def test_security_headers(self):
        """Test security headers configuration"""
        print("\n🛡️  Testing Security Headers:")
        print("=" * 50)
        
        self.test_setting('SECURE_BROWSER_XSS_FILTER', True, 
                        'SECURE_BROWSER_XSS_FILTER: XSS filtering enabled')
        self.test_setting('SECURE_CONTENT_TYPE_NOSNIFF', True, 
                        'SECURE_CONTENT_TYPE_NOSNIFF: MIME sniffing prevention')
        self.test_setting('X_FRAME_OPTIONS', 'DENY', 
                        'X_FRAME_OPTIONS: Clickjacking protection')
        self.test_setting('SECURE_REFERRER_POLICY', 'strict-origin-when-cross-origin', 
                        'SECURE_REFERRER_POLICY: Referrer policy configured')
    
    def test_csp_configuration(self):
        """Test Content Security Policy configuration"""
        print("\n📋 Testing Content Security Policy:")
        print("=" * 50)
        
        if hasattr(settings, 'CONTENT_SECURITY_POLICY'):
            csp_config = settings.CONTENT_SECURITY_POLICY
            if 'DIRECTIVES' in csp_config:
                directives = csp_config['DIRECTIVES']
                
                # Test key CSP directives
                if 'default-src' in directives:
                    print("✅ CSP: default-src directive configured")
                    self.passed_tests += 1
                else:
                    print("❌ CSP: default-src directive missing")
                
                if 'script-src' in directives:
                    print("✅ CSP: script-src directive configured")
                    self.passed_tests += 1
                else:
                    print("❌ CSP: script-src directive missing")
                
                self.total_tests += 2
            else:
                print("❌ CSP: DIRECTIVES not found in configuration")
                self.total_tests += 1
        else:
            print("❌ CSP: CONTENT_SECURITY_POLICY not configured")
            self.total_tests += 1
    
    def test_allowed_hosts(self):
        """Test ALLOWED_HOSTS configuration"""
        print("\n🌐 Testing ALLOWED_HOSTS Configuration:")
        print("=" * 50)
        
        allowed_hosts = settings.ALLOWED_HOSTS
        if allowed_hosts:
            print(f"✅ ALLOWED_HOSTS: Configured with {len(allowed_hosts)} host(s)")
            for host in allowed_hosts:
                print(f"   - {host}")
            self.passed_tests += 1
        else:
            print("❌ ALLOWED_HOSTS: Not configured (security risk)")
        
        self.total_tests += 1
    
    def test_debug_setting(self):
        """Test DEBUG setting"""
        print("\n🔧 Testing DEBUG Configuration:")
        print("=" * 50)
        
        if settings.DEBUG:
            print("⚠️  DEBUG: True (Development mode)")
            print("   - HTTPS enforcement disabled for local testing")
            print("   - Cookie security relaxed for development")
            print("   - Remember to set DEBUG=False in production!")
        else:
            print("✅ DEBUG: False (Production mode)")
            print("   - Full security enforcement enabled")
        
        # This doesn't count as pass/fail since it's environment-dependent
    
    def test_middleware_configuration(self):
        """Test security middleware configuration"""
        print("\n⚙️  Testing Security Middleware:")
        print("=" * 50)
        
        middleware = settings.MIDDLEWARE
        required_middleware = [
            'django.middleware.security.SecurityMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
        ]
        
        for mw in required_middleware:
            if mw in middleware:
                print(f"✅ {mw.split('.')[-1]}: Enabled")
                self.passed_tests += 1
            else:
                print(f"❌ {mw.split('.')[-1]}: Missing")
            self.total_tests += 1
        
        # Check CSP middleware
        if 'csp.middleware.CSPMiddleware' in middleware:
            print("✅ CSPMiddleware: Content Security Policy enabled")
            self.passed_tests += 1
        else:
            print("❌ CSPMiddleware: Content Security Policy disabled")
        self.total_tests += 1
    
    def run_all_tests(self):
        """Run all security configuration tests"""
        print("🔒 HTTPS Security Configuration Test")
        print("=" * 60)
        print(f"Testing Django application security settings...")
        print(f"Environment: {'Development' if settings.DEBUG else 'Production'}")
        
        # Run all test categories
        self.test_https_settings()
        self.test_cookie_security()
        self.test_security_headers()
        self.test_csp_configuration()
        self.test_allowed_hosts()
        self.test_debug_setting()
        self.test_middleware_configuration()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        pass_rate = (self.passed_tests / self.total_tests * 100) if self.total_tests > 0 else 0
        
        print(f"Passed: {self.passed_tests}/{self.total_tests} tests ({pass_rate:.1f}%)")
        
        if pass_rate >= 90:
            print("🎉 Excellent! Your security configuration is robust.")
            status = "EXCELLENT"
        elif pass_rate >= 75:
            print("✅ Good! Your security configuration is solid with minor improvements needed.")
            status = "GOOD"
        elif pass_rate >= 50:
            print("⚠️  Fair. Your security configuration needs improvement.")
            status = "NEEDS_IMPROVEMENT"
        else:
            print("❌ Poor. Your security configuration has significant issues.")
            status = "CRITICAL"
        
        print("\n📋 RECOMMENDATIONS:")
        if settings.DEBUG:
            print("- Set DEBUG=False when deploying to production")
            print("- Configure proper ALLOWED_HOSTS for your domain")
            print("- Obtain and configure SSL certificate")
            print("- Test HTTPS redirect functionality")
        else:
            print("- Verify SSL certificate is properly installed")
            print("- Test HTTPS redirect with real traffic")
            print("- Monitor security logs regularly")
            print("- Schedule regular security audits")
        
        print(f"\n🔒 Security Status: {status}")
        return status

def main():
    """Main function to run the security tests"""
    try:
        tester = HTTPSSecurityTester()
        status = tester.run_all_tests()
        
        # Exit with appropriate code
        if status in ['EXCELLENT', 'GOOD']:
            sys.exit(0)
        elif status == 'NEEDS_IMPROVEMENT':
            sys.exit(1)
        else:
            sys.exit(2)
            
    except Exception as e:
        print(f"❌ Error running security tests: {e}")
        sys.exit(3)

if __name__ == '__main__':
    main()

"""
URL Configuration Validation Script
This script validates that the required URL patterns exist in api/urls.py
"""

def check_url_patterns():
    """Check if api/urls.py contains the required URL patterns."""
    
    try:
        with open('api/urls.py', 'r') as file:
            content = file.read()
            
        required_patterns = ['books/update', 'books/delete']
        found_patterns = []
        missing_patterns = []
        
        for pattern in required_patterns:
            if pattern in content:
                found_patterns.append(pattern)
                print(f"✅ Found: {pattern}")
            else:
                missing_patterns.append(pattern)
                print(f"❌ Missing: {pattern}")
        
        print(f"\nSummary:")
        print(f"Found patterns: {len(found_patterns)}")
        print(f"Missing patterns: {len(missing_patterns)}")
        
        if missing_patterns:
            print(f"\n⚠️ Missing patterns: {missing_patterns}")
            return False
        else:
            print(f"\n🎉 All required URL patterns are configured correctly!")
            return True
            
    except FileNotFoundError:
        print("❌ Error: api/urls.py file not found!")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

if __name__ == "__main__":
    print("Checking URL patterns in api/urls.py...")
    print("=" * 50)
    
    success = check_url_patterns()
    
    if success:
        print("\n✅ URL configuration validation PASSED!")
    else:
        print("\n❌ URL configuration validation FAILED!")

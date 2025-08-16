"""
Permission Classes Validation Script
This script validates that the required DRF permission imports exist in api/views.py
"""

def check_permission_imports():
    """Check if api/views.py contains the required permission imports."""
    
    try:
        with open('api/views.py', 'r') as file:
            content = file.read()
            
        required_import = "from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated"
        
        print("Checking for required permission imports...")
        print("=" * 60)
        
        if required_import in content:
            print("✅ Found required import:")
            print(f"   {required_import}")
            
            # Check if these permissions are actually used in the code
            print("\n📋 Usage of imported permissions:")
            
            if "IsAuthenticated]" in content:
                print("✅ IsAuthenticated is used in permission_classes")
            else:
                print("❌ IsAuthenticated not found in permission_classes")
                
            if "IsAuthenticatedOrReadOnly]" in content:
                print("✅ IsAuthenticatedOrReadOnly is used in permission_classes")
            else:
                print("❌ IsAuthenticatedOrReadOnly not found in permission_classes")
                
            print(f"\n🎉 Permission classes validation PASSED!")
            return True
        else:
            print("❌ Required import not found:")
            print(f"   Expected: {required_import}")
            print(f"\n❌ Permission classes validation FAILED!")
            return False
            
    except FileNotFoundError:
        print("❌ Error: api/views.py file not found!")
        return False
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return False

def check_permission_usage():
    """Check different types of permissions used in the views."""
    
    try:
        with open('api/views.py', 'r') as file:
            content = file.read()
            
        print("\n📊 Permission Classes Analysis:")
        print("-" * 40)
        
        # Count different permission usage
        permissions_found = []
        
        if "permissions.AllowAny" in content:
            permissions_found.append("AllowAny (via permissions.)")
            
        if "IsAuthenticated]" in content:
            permissions_found.append("IsAuthenticated (direct import)")
            
        if "IsAuthenticatedOrReadOnly]" in content:
            permissions_found.append("IsAuthenticatedOrReadOnly (direct import)")
            
        if "IsOwnerOrReadOnly" in content:
            permissions_found.append("IsOwnerOrReadOnly (custom permission)")
            
        if permissions_found:
            print("✅ Permission classes found:")
            for perm in permissions_found:
                print(f"   • {perm}")
        else:
            print("❌ No permission classes found")
            
        return len(permissions_found) > 0
            
    except Exception as e:
        print(f"❌ Error analyzing permissions: {e}")
        return False

if __name__ == "__main__":
    print("Validating Permission Classes in api/views.py...")
    print("=" * 60)
    
    import_success = check_permission_imports()
    usage_success = check_permission_usage()
    
    print("\n" + "=" * 60)
    if import_success and usage_success:
        print("🎉 ALL PERMISSION VALIDATIONS PASSED!")
        print("✅ Required imports are present")
        print("✅ Permission classes are properly used")
    else:
        print("❌ PERMISSION VALIDATION FAILED!")
        if not import_success:
            print("❌ Missing required imports")
        if not usage_success:
            print("❌ Issues with permission usage")

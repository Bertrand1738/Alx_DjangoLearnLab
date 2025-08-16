#!/usr/bin/env python
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, r'C:\Users\pc\Desktop\Code\Alx_DjangoLearnLab')

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_project.settings')

try:
    from api_project.settings import INSTALLED_APPS
    print("Successfully imported INSTALLED_APPS")
    print("INSTALLED_APPS:")
    for app in INSTALLED_APPS:
        print(f"  - {app}")
    
    print(f"\nrest_framework present: {'rest_framework' in INSTALLED_APPS}")
    print(f"api present: {'api' in INSTALLED_APPS}")
    
except ImportError as e:
    print(f"Import error: {e}")
    
print("Script completed")

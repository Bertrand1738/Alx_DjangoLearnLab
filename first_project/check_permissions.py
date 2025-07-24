import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'first_project.settings')
django.setup()

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from book_store.models import Product

# Get content type for Product model
content_type = ContentType.objects.get_for_model(Product)
print(f'Content type: {content_type}')

# Check all permissions for this content type
permissions = Permission.objects.filter(content_type=content_type)
print('All permissions for Product model:')
for perm in permissions:
    print(f'  - {perm.codename}: {perm.name}')

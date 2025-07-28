from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Test the custom user model by creating a sample user'

    def handle(self, *args, **options):
        # Test our custom user model
        self.stdout.write(self.style.SUCCESS('🧪 Testing Custom User Model...'))
        
        # Check if our CustomUser model is being used
        self.stdout.write(f'✅ Using user model: {User.__name__}')
        self.stdout.write(f'✅ User model module: {User._meta.app_label}.{User._meta.model_name}')
        
        # Check available fields
        custom_fields = []
        for field in User._meta.fields:
            if field.name in ['date_of_birth', 'profile_photo']:
                custom_fields.append(field.name)
        
        if custom_fields:
            self.stdout.write(f'✅ Custom fields found: {", ".join(custom_fields)}')
        else:
            self.stdout.write(self.style.ERROR('❌ Custom fields not found!'))
            return
        
        # Try to create a test user
        test_username = 'testuser_custom'
        
        # Delete test user if exists
        if User.objects.filter(username=test_username).exists():
            User.objects.filter(username=test_username).delete()
            self.stdout.write('🗑️  Deleted existing test user')
        
        # Create test user with custom fields
        try:
            user = User.objects.create_user(
                username=test_username,
                email='test@example.com',
                password='testpass123',
                date_of_birth=date(1990, 1, 1),
                first_name='Test',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS(f'✅ Successfully created user: {user.username}'))
            self.stdout.write(f'   📧 Email: {user.email}')
            self.stdout.write(f'   🎂 Date of birth: {user.date_of_birth}')
            self.stdout.write(f'   📸 Profile photo: {user.profile_photo or "Not set"}')
            
            # Clean up
            user.delete()
            self.stdout.write('🧹 Cleaned up test user')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating user: {e}'))
            return
        
        self.stdout.write(self.style.SUCCESS('🎉 Custom User Model is working perfectly!'))

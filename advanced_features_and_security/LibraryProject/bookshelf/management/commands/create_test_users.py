from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

class Command(BaseCommand):
    help = 'Create test users and assign them to groups for permission testing'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('👥 Creating test users...'))
        
        # Get the groups
        try:
            viewers_group = Group.objects.get(name='Viewers')
            editors_group = Group.objects.get(name='Editors')
            admins_group = Group.objects.get(name='Admins')
        except Group.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Groups not found! Please run: python manage.py setup_permissions'))
            return
        
        # Create test users
        users_data = [
            {
                'username': 'viewer_user',
                'email': 'viewer@example.com',
                'password': 'testpass123',
                'group': viewers_group,
                'description': 'Can only view books'
            },
            {
                'username': 'editor_user',
                'email': 'editor@example.com',
                'password': 'testpass123',
                'group': editors_group,
                'description': 'Can view, create, and edit books'
            },
            {
                'username': 'admin_user',
                'email': 'admin@example.com',
                'password': 'testpass123',
                'group': admins_group,
                'description': 'Can do everything with books'
            }
        ]
        
        for user_data in users_data:
            # Delete user if exists
            if User.objects.filter(username=user_data['username']).exists():
                User.objects.filter(username=user_data['username']).delete()
                self.stdout.write(f'🗑️  Deleted existing user: {user_data["username"]}')
            
            # Create user
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password'],
                first_name=user_data['username'].replace('_', ' ').title(),
            )
            
            # Add to group
            user.groups.add(user_data['group'])
            
            self.stdout.write(f'✅ Created user: {user.username} -> {user_data["group"].name}')
            self.stdout.write(f'   📧 Email: {user.email}')
            self.stdout.write(f'   🔐 Password: {user_data["password"]}')
            self.stdout.write(f'   📝 Description: {user_data["description"]}')
            self.stdout.write('')
        
        self.stdout.write(self.style.SUCCESS('🎉 Test users created successfully!'))
        self.stdout.write('\n📋 Testing Guide:')
        self.stdout.write('1. Start the server: python manage.py runserver')
        self.stdout.write('2. Visit: http://127.0.0.1:8000/bookshelf/books/')
        self.stdout.write('3. Login with different users to test permissions')
        self.stdout.write('4. Check permissions at: http://127.0.0.1:8000/bookshelf/permissions/')
        self.stdout.write('\n🔑 Test Credentials:')
        for user_data in users_data:
            self.stdout.write(f'   {user_data["username"]} / {user_data["password"]} ({user_data["group"].name})')

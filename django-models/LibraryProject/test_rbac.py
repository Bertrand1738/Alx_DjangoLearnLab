# Script to test role-based access control
# Run: python manage.py shell < test_rbac.py

from django.contrib.auth.models import User
from relationship_app.models import UserProfile

print("🔐 Testing Role-Based Access Control")
print("=" * 50)

# Create test users with different roles
print("\n1️⃣ Creating test users...")

# Clear existing test users
User.objects.filter(username__in=['admin_user', 'librarian_user', 'member_user']).delete()

# Create Admin user
admin_user = User.objects.create_user(
    username='admin_user',
    password='testpass123',
    email='admin@library.com'
)
# The UserProfile is created automatically by our signal
admin_user.userprofile.role = 'Admin'
admin_user.userprofile.save()
print(f"✅ Created Admin: {admin_user.username} - {admin_user.userprofile.role}")

# Create Librarian user
librarian_user = User.objects.create_user(
    username='librarian_user', 
    password='testpass123',
    email='librarian@library.com'
)
librarian_user.userprofile.role = 'Librarian'
librarian_user.userprofile.save()
print(f"✅ Created Librarian: {librarian_user.username} - {librarian_user.userprofile.role}")

# Create Member user  
member_user = User.objects.create_user(
    username='member_user',
    password='testpass123', 
    email='member@library.com'
)
member_user.userprofile.role = 'Member'
member_user.userprofile.save()
print(f"✅ Created Member: {member_user.username} - {member_user.userprofile.role}")

print("\n2️⃣ User Profiles Created:")
for profile in UserProfile.objects.all():
    print(f"   • {profile.user.username}: {profile.role}")

print("\n🎉 Role-Based Access Control Setup Complete!")
print("\nTest the system:")
print("1. Login with 'admin_user' / 'testpass123' → Visit /relationship_app/admin_view/")
print("2. Login with 'librarian_user' / 'testpass123' → Visit /relationship_app/librarian_view/")
print("3. Login with 'member_user' / 'testpass123' → Visit /relationship_app/member_view/")
print("\nTry accessing wrong role pages to test access restrictions!")

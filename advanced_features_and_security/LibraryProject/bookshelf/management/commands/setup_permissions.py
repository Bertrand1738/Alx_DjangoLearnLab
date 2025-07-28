from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book

class Command(BaseCommand):
    help = 'Create user groups and assign permissions'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔐 Setting up Groups and Permissions...'))
        
        # Get the Book content type
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get our custom permissions
        try:
            can_view = Permission.objects.get(codename='can_view', content_type=book_content_type)
            can_create = Permission.objects.get(codename='can_create', content_type=book_content_type)
            can_edit = Permission.objects.get(codename='can_edit', content_type=book_content_type)
            can_delete = Permission.objects.get(codename='can_delete', content_type=book_content_type)
            self.stdout.write('✅ Found all custom permissions')
        except Permission.DoesNotExist as e:
            self.stdout.write(self.style.ERROR(f'❌ Permission not found: {e}'))
            return

        # Create Viewers group
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        if created:
            self.stdout.write('📖 Created Viewers group')
        else:
            self.stdout.write('📖 Viewers group already exists')
        
        # Assign permissions to Viewers (only view)
        viewers_group.permissions.clear()
        viewers_group.permissions.add(can_view)
        self.stdout.write('   ✅ Viewers can: view books')

        # Create Editors group
        editors_group, created = Group.objects.get_or_create(name='Editors')
        if created:
            self.stdout.write('✏️  Created Editors group')
        else:
            self.stdout.write('✏️  Editors group already exists')
        
        # Assign permissions to Editors (view, create, edit)
        editors_group.permissions.clear()
        editors_group.permissions.add(can_view, can_create, can_edit)
        self.stdout.write('   ✅ Editors can: view, create, edit books')

        # Create Admins group
        admins_group, created = Group.objects.get_or_create(name='Admins')
        if created:
            self.stdout.write('👑 Created Admins group')
        else:
            self.stdout.write('👑 Admins group already exists')
        
        # Assign all permissions to Admins
        admins_group.permissions.clear()
        admins_group.permissions.add(can_view, can_create, can_edit, can_delete)
        self.stdout.write('   ✅ Admins can: view, create, edit, delete books')

        self.stdout.write(self.style.SUCCESS('\n🎉 Groups and permissions setup complete!'))
        self.stdout.write('\n📋 Summary:')
        self.stdout.write('   👁️  Viewers: can_view')
        self.stdout.write('   ✏️  Editors: can_view, can_create, can_edit')
        self.stdout.write('   👑 Admins: can_view, can_create, can_edit, can_delete')
        self.stdout.write('\n💡 Next: Assign users to groups in Django admin!')

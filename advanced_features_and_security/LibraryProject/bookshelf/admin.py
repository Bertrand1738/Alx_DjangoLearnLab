from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

# Custom User Admin Configuration
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for our CustomUser model.
    This tells Django how to display users in the admin panel.
    """
    # What columns to show in the user list
    list_display = ('username', 'email', 'first_name', 'last_name', 'date_of_birth', 'is_staff')
    
    # What filters to add on the side panel
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'date_of_birth')
    
    # What fields can be searched
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    # Order users by username
    ordering = ('username',)
    
    # Configure the form layout for editing existing users
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )
    
    # Configure the form layout for adding new users
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Information', {
            'fields': ('date_of_birth', 'profile_photo')
        }),
    )

# Register our models with the admin
admin.site.register(CustomUser, CustomUserAdmin)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('publication_year', 'author')
    search_fields = ('title', 'author')
    
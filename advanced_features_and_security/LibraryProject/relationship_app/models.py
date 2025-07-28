from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Author(models.Model):
    """Author model with a name field"""
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class Book(models.Model):
    """Book model with title and ForeignKey relationship to Author"""
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    
    class Meta:
        """
        Meta class for Book model with custom permissions.
        
        BEGINNER EXPLANATION:
        - Meta class provides metadata about the model
        - permissions tuple defines custom permissions for this model
        - Each permission has a code name and human-readable description
        - These permissions can be assigned to users or groups
        """
        permissions = [
            ("can_add_book", "Can add book"),
            ("can_change_book", "Can change book"),
            ("can_delete_book", "Can delete book"),
        ]
    
    def __str__(self):
        return self.title


class Library(models.Model):
    """Library model with name and ManyToMany relationship to Book"""
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book)
    
    def __str__(self):
        return self.name


class Librarian(models.Model):
    """Librarian model with name and OneToOne relationship to Library"""
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    """
    UserProfile model to extend Django's built-in User model with role-based access control.
    
    BEGINNER EXPLANATION:
    - This model extends Django's User with additional information
    - OneToOneField means each User has exactly one UserProfile
    - Role field determines what the user can access in the application
    - Choices limit the role to specific predefined values
    """
    
    # Role choices for the application
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]
    
    # Link to Django's User model (now our custom user)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    # Role field with predefined choices
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Member')
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"


# =============================================================================
# DJANGO SIGNALS FOR AUTOMATIC USERPROFILE CREATION
# =============================================================================

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create a UserProfile when a new User is created.
    
    BEGINNER EXPLANATION:
    - This function runs automatically when a User is saved
    - @receiver decorator connects this function to the User model
    - post_save signal fires after a User is successfully saved
    - created=True means this is a new user, not an update
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)  
def save_user_profile(sender, instance, **kwargs):
    """
    Automatically save the UserProfile when the User is saved.
    
    BEGINNER EXPLANATION:
    - This ensures the UserProfile is always saved when User is saved
    - Handles cases where UserProfile might exist but needs updating
    """
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
    else:
        # Create profile if it doesn't exist (safety check)
        UserProfile.objects.create(user=instance)

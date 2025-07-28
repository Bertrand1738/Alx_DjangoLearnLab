from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

# Step 1: Create a Custom User Manager (This helps create users properly)
class CustomUserManager(BaseUserManager):
    """
    Custom manager for our CustomUser model.
    This class knows how to create regular users and superusers.
    """
    def create_user(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a regular user with username, email and password.
        """
        # Make sure username is provided
        if not username:
            raise ValueError('The Username field must be set')
        
        # Clean up the email address
        if email:
            email = self.normalize_email(email)
        
        # Set default values for permissions
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        
        # Create the user instance
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # This encrypts the password
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """
        Create and return a superuser with admin privileges.
        """
        # Set required permissions for superuser
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        # Double-check the permissions are correct
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, password, **extra_fields)

# Step 2: Create the Custom User Model
class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    Adds date_of_birth and profile_photo fields.
    """
    # Our new fields
    date_of_birth = models.DateField(
        null=True,      # Can be empty in database
        blank=True,     # Can be empty in forms
        help_text="User's date of birth"
    )
    
    profile_photo = models.ImageField(
        upload_to='profile_photos/',  # Folder where images will be saved
        null=True,      # Can be empty in database
        blank=True,     # Can be empty in forms
        help_text="User's profile photo"
    )
    
    # Use our custom manager
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

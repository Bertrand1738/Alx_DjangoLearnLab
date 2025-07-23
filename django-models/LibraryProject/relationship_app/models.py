from django.db import models

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

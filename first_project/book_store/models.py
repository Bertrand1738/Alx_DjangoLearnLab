from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50)

    class Meta:
        permissions = [
            ("can_view_all_products", "Can view all products"),
            ("can_manage_inventory", "Can manage inventory"),
            ("can_set_prices", "Can set product prices"),
        ]

    def __str__(self):
        return self.name

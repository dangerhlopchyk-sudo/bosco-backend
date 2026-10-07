from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    vehicle_brand = models.CharField(max_length=100)
    part_number = models.CharField(max_length=50)
    origin_country = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} ({self.part_number})"

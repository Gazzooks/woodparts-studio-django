# materials/models.py
from django.db import models

class StockMaterial(models.Model):
    material = models.CharField(max_length=100)
    length = models.FloatField()
    width = models.FloatField()
    thickness = models.FloatField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.material} ({self.length}x{self.width}x{self.thickness})"

from django.db import models
from projects.models import Project
from materials.models import StockMaterial

class Cutlist(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='cutlists')
    name = models.CharField(max_length=255)
    datecreated = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.datecreated:%Y-%m-%d})"

class CutlistPart(models.Model):
    cutlist = models.ForeignKey(Cutlist, on_delete=models.CASCADE, related_name='parts')
    partname = models.CharField(max_length=255)  # Note the field name from schema
    length = models.DecimalField(max_digits=10, decimal_places=4)
    width = models.DecimalField(max_digits=10, decimal_places=4)
    thickness = models.DecimalField(max_digits=10, decimal_places=4)
    material = models.ForeignKey(StockMaterial, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    angle = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    orientation = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['partname']

    def __str__(self):
        return f"{self.partname} ({self.length}x{self.width}x{self.thickness})"

class CutlistStock(models.Model):
    cutlist = models.ForeignKey(Cutlist, on_delete=models.CASCADE, related_name='stock_materials')
    material = models.CharField(max_length=255)
    length = models.DecimalField(max_digits=10, decimal_places=4)
    width = models.DecimalField(max_digits=10, decimal_places=4)
    thickness = models.DecimalField(max_digits=10, decimal_places=4)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.material} ({self.length}\"x{self.width}\"x{self.thickness}\")"

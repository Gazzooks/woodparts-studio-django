from django.db import models
from projects.models import Project
from materials.models import StockMaterial

class Part(models.Model):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='parts')
    material = models.ForeignKey(StockMaterial, on_delete=models.SET_NULL, null=True, blank=True)
    length = models.DecimalField(max_digits=10, decimal_places=4)
    width = models.DecimalField(max_digits=10, decimal_places=4)
    thickness = models.DecimalField(max_digits=10, decimal_places=4)
    quantity = models.PositiveIntegerField(default=1)
    notes = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return f"{self.name} ({self.project.name})"

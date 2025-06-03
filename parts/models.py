from django.db import models
from django.core.validators import MinValueValidator
from core.models import TimeStampedModel
from projects.models import Project

class Part(TimeStampedModel):
    """Part model - maps to your existing parts table"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='parts')
    partname = models.CharField(max_length=200, db_index=True)  # Keep original field name
    length = models.DecimalField(max_digits=10, decimal_places=4, validators=[MinValueValidator(0)])
    width = models.DecimalField(max_digits=10, decimal_places=4, validators=[MinValueValidator(0)])
    thickness = models.DecimalField(max_digits=10, decimal_places=4, validators=[MinValueValidator(0)])
    material = models.CharField(max_length=100, db_index=True)
    quantity = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    angle = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    orientation = models.CharField(max_length=50, blank=True)
    notes = models.TextField(blank=True)
    
    # Additional fields for enhanced functionality
    category = models.CharField(max_length=100, blank=True, db_index=True)
    priority = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['partname']
        indexes = [
            models.Index(fields=['project', 'partname']),
            models.Index(fields=['material']),
            models.Index(fields=['category']),
        ]
        
    def __str__(self):
        return f"{self.partname} ({self.project.name})"
    
    @property
    def board_feet(self):
        """Calculate board feet for this part"""
        return (self.length * self.width * self.thickness * self.quantity) / 144
    
    @property
    def volume_cubic_inches(self):
        """Calculate volume in cubic inches"""
        return self.length * self.width * self.thickness * self.quantity

class PartTemplate(TimeStampedModel):
    """Reusable part templates"""
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    length = models.DecimalField(max_digits=10, decimal_places=4)
    width = models.DecimalField(max_digits=10, decimal_places=4)
    thickness = models.DecimalField(max_digits=10, decimal_places=4)
    material = models.CharField(max_length=100)
    category = models.CharField(max_length=100, blank=True)
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['category', 'name']
    
    def __str__(self):
        return self.name

class PartHistory(TimeStampedModel):
    """Track changes to parts"""
    part = models.ForeignKey(Part, on_delete=models.CASCADE, related_name='history')
    changed_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    change_type = models.CharField(max_length=20)  # 'created', 'updated', 'deleted'
    changes = models.JSONField(default=dict)  # Store what changed
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.part.partname} - {self.change_type} by {self.changed_by.username}"
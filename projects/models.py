from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import TimeStampedModel

class Project(TimeStampedModel):
    """Main project model - maps to your existing projects table"""
    STATUS_CHOICES = [
        ('planning', 'Planning'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('archived', 'Archived'),
    ]
    
    name = models.CharField(max_length=200, db_index=True)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning', db_index=True)
    notes = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    
    # Migration from your existing fields - keep original names for easier migration
    datecreated = models.DateTimeField(auto_now_add=True)  # Maps to your datecreated
    datemodified = models.DateTimeField(auto_now=True)     # Maps to your datemodified
    
    class Meta:
        ordering = ['-datemodified']
        indexes = [
            models.Index(fields=['owner', '-datemodified']),
            models.Index(fields=['status']),
        ]
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'pk': self.pk})
    
    @property
    def total_parts(self):
        return self.parts.count()
    
    @property
    def total_quantity(self):
        return sum(part.quantity for part in self.parts.all())
    
    @property
    def unique_materials(self):
        return self.parts.values('material').distinct().count()
    
    @property
    def total_board_feet(self):
        """Calculate total board feet for all parts"""
        total = 0
        for part in self.parts.all():
            total += part.board_feet
        return total

class ProjectSettings(models.Model):
    """Project-specific settings"""
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name='settings')
    default_material = models.CharField(max_length=100, blank=True)
    default_thickness = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True)
    cut_optimization_enabled = models.BooleanField(default=True)
    measurement_units = models.CharField(max_length=20, default='imperial')
    
    def __str__(self):
        return f"Settings for {self.project.name}"

class ProjectTimeline(TimeStampedModel):
    """Project timeline and milestones"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='timeline')
    milestone = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    target_date = models.DateField(null=True, blank=True)
    completed_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['target_date']
    
    def __str__(self):
        return f"{self.project.name}: {self.milestone}"

class ProjectNote(TimeStampedModel):
    """Project notes and documentation"""
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_notes')
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=50, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.project.name}: {self.title}"
from django.db import models
from django.contrib.auth.models import User

class TimeStampedModel(models.Model):
    """Abstract base class with created/modified timestamps"""
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class UserPreference(models.Model):
    """User preferences and settings"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_units = models.CharField(max_length=20, default='imperial')
    theme = models.CharField(max_length=20, default='light')
    auto_save = models.BooleanField(default=True)
    window_positions = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.user.username} preferences"

class ApplicationSetting(models.Model):
    """Global application settings"""
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.key}: {self.value}"

class RecentFile(models.Model):
    """Track recent files/databases opened by users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=500)
    file_name = models.CharField(max_length=255)
    last_accessed = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-last_accessed']
        unique_together = ['user', 'file_path']
    
    def __str__(self):
        return f"{self.user.username}: {self.file_name}"
# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class UserPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=20, default='light', choices=[
        ('light', 'Light Theme'),
        ('dark', 'Dark Theme')
    ])
    default_units = models.CharField(max_length=10, default='metric', choices=[
        ('imperial', 'Imperial (inches)'),
        ('metric', 'Metric (mm)')
    ])
    autosave_interval = models.IntegerField(default=5)
    show_tutorial = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"

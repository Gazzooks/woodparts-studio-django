# accounts/forms.py
from django import forms
from .models import UserPreferences

class PreferencesForm(forms.ModelForm):
    class Meta:
        model = UserPreferences
        fields = ['theme', 'default_units', 'autosave_interval', 'show_tutorial']
        widgets = {
            'autosave_interval': forms.NumberInput(attrs={'min': 1, 'max': 60}),
        }

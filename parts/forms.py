# parts/forms.py
from django import forms
from .models import Part

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = '__all__'
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

# parts/forms.py
from django import forms
from .models import Part, PartTemplate

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = [
            'partname', 'length', 'width', 'thickness',
            'material', 'quantity', 'angle', 'orientation', 'notes'
        ]
        widgets = {
            'length': forms.NumberInput(attrs={'step': '0.01'}),
            'width': forms.NumberInput(attrs={'step': '0.01'}),
            'thickness': forms.NumberInput(attrs={'step': '0.01'}),
            'angle': forms.NumberInput(attrs={'step': '0.1'}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class BulkPartForm(forms.Form):
    material = forms.CharField(required=False)
    category = forms.CharField(required=False)
    selected_parts = forms.ModelMultipleChoiceField(
        queryset=Part.objects.all(),
        widget=forms.MultipleHiddenInput
    )

class PartTemplateForm(forms.ModelForm):
    class Meta:
        model = PartTemplate
        fields = ['name', 'description', 'length', 'width', 
                 'thickness', 'material', 'category']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

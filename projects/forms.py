from django import forms
from .models import Project, ProjectSettings, ProjectNote

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'status', 'notes']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }

class ProjectSettingsForm(forms.ModelForm):
    class Meta:
        model = ProjectSettings
        fields = ['default_material', 'default_thickness', 'cut_optimization_enabled']
        widgets = {
            'default_thickness': forms.NumberInput(attrs={'step': '0.01'}),
        }

class ProjectNoteForm(forms.ModelForm):
    class Meta:
        model = ProjectNote
        fields = ['title', 'content', 'category']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6}),
        }

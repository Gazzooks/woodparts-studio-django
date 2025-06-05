# parts/forms.py
from django import forms
from .models import Part
from materials.models import StockMaterial
from accounts.models import UserPreferences

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['name', 'project', 'material', 'length', 'width', 'thickness', 'quantity', 'notes']
        # ^-- Include all fields you want to collect

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user and hasattr(user, 'userpreferences'):
            unit_system = user.userpreferences.default_units
            self.fields['material'].queryset = StockMaterial.objects.filter(unit_system=unit_system)
        self.fields['material'].label_from_instance = self.label_from_instance

    @staticmethod
    def label_from_instance(obj):
        return f"{obj.material} – {obj.notes} ({obj.unit_system})"

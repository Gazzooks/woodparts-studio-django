# parts/forms.py
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div, Row, Column, Submit
from django import forms
from .models import Part
from materials.models import StockMaterial
from accounts.models import UserPreferences

class PartForm(forms.ModelForm):
    class Meta:
        model = Part
        fields = ['name', 'material', 'length', 'width', 'thickness', 'quantity', 'notes']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='col-md-6 mb-3'),
                Column('material', css_class='col-md-6 mb-3'),
            ),
            Row(
                Column('length', css_class='col-md-4 mb-3'),
                Column('width', css_class='col-md-4 mb-3'),
                Column('thickness', css_class='col-md-4 mb-3'),
            ),
            Field('quantity', css_class='mb-3'),
            # Notes field full width
            Field('notes', css_class='mb-3 w-100'),
        )

    @staticmethod
    def label_from_instance(obj):
        return f"{obj.material} – {obj.notes} ({obj.unit_system})"

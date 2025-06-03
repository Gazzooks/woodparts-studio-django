from django import forms
from django.forms import inlineformset_factory
from .models import Cutlist, CutlistPart, CutlistStock

class CutlistForm(forms.ModelForm):
    class Meta:
        model = Cutlist
        fields = ['name', 'notes']

CutlistPartFormSet = inlineformset_factory(
    Cutlist,
    CutlistPart,
    fields=(
        'partname',  # Correct field name from model
        'length', 
        'width', 
        'thickness', 
        'material', 
        'quantity', 
        'notes',
        'angle',
        'orientation'
    ),
    extra=1,
    can_delete=True
)

CutlistStockFormSet = inlineformset_factory(
    Cutlist,
    CutlistStock,
    fields=('material', 'length', 'width', 'thickness', 'quantity', 'price'),
    extra=1,
    can_delete=True
)

from django import forms
from .models import Tool, ToolMaintenance

TOOL_TYPE_CHOICES = [
    ('Table Saw', 'Table Saw'),
    ('Miter Saw', 'Miter Saw'),
    ('Band Saw', 'Band Saw'),
    ('Jointer', 'Jointer'),
    ('Planer', 'Planer'),
    ('Drill Press', 'Drill Press'),
    ('Router', 'Router'),
    ('Circular Saw', 'Circular Saw'),
    ('Jigsaw', 'Jigsaw'),
    ('Scroll Saw', 'Scroll Saw'),
    ('Lathe', 'Lathe'),
    ('Belt Sander', 'Belt Sander'),
    ('Orbital Sander', 'Orbital Sander'),
    ('Hand Saw', 'Hand Saw'),
    ('Chisel', 'Chisel'),
    ('Clamps', 'Clamps'),
    ('Hammer', 'Hammer'),
    ('Tape Measure', 'Tape Measure'),
    ('Square', 'Square'),
    ('Dust Collector', 'Dust Collector'),
]

TOOL_BRAND_CHOICES = [
    ('DeWalt', 'DeWalt'),
    ('Makita', 'Makita'),
    ('Bosch', 'Bosch'),
    ('Milwaukee', 'Milwaukee'),
    ('Festool', 'Festool'),
    ('Ridgid', 'Ridgid'),
    ('Ryobi', 'Ryobi'),
    ('Jet', 'Jet'),
    ('Grizzly', 'Grizzly'),
    ('Delta', 'Delta'),
    ('Porter-Cable', 'Porter-Cable'),
    ('Craftsman', 'Craftsman'),
    ('Hitachi/Metabo HPT', 'Hitachi/Metabo HPT'),
    ('Rikon', 'Rikon'),
    ('Laguna', 'Laguna'),
]

TOOL_LOCATION_CHOICES = [
    ('Tool Wall', 'Tool Wall'),
    ('Tool Cabinet', 'Tool Cabinet'),
    ('Drawer', 'Drawer'),
    ('Pegboard', 'Pegboard'),
    ('Shelf', 'Shelf'),
    ('Workbench', 'Workbench'),
    ('Rolling Cart', 'Rolling Cart'),
    ('Upper Cabinet', 'Upper Cabinet'),
    ('Base Cabinet', 'Base Cabinet'),
    ('Lumber Rack', 'Lumber Rack'),
]

MAINTENANCE_TYPE_CHOICES = [
    ('Routine', 'Routine'),
    ('Repair', 'Repair'),
    ('Calibration', 'Calibration'),
    ('Cleaning', 'Cleaning'),
    ('Replacement', 'Replacement'),
    ('Inspection', 'Inspection'),
    ('Other', 'Other'),
]

class ToolForm(forms.ModelForm):
    type = forms.ChoiceField(
        choices=TOOL_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    brand = forms.ChoiceField(
        choices=TOOL_BRAND_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.ChoiceField(
        choices=TOOL_LOCATION_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Tool
        fields = [
            'name',
            'type',
            'serial_number',
            'brand',
            'model',
            'purchase_date',
            'purchase_price',
            'location',
            'notes',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'model': forms.TextInput(attrs={'class': 'form-control'}),
            'purchase_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'purchase_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            # If the widget already has a class, append to it
            existing_classes = visible.field.widget.attrs.get('class', '')
            visible.field.widget.attrs['class'] = (existing_classes + ' form-control').strip()


class ToolMaintenanceForm(forms.ModelForm):
    maintenance_type = forms.ChoiceField(
        choices=MAINTENANCE_TYPE_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = ToolMaintenance
        fields = [
            'tool',
            'maintenance_date',
            'maintenance_type',
            'notes',
        ]
        widgets = {
            'tool': forms.Select(attrs={'class': 'form-control'}),
            'maintenance_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class ToolImportForm(forms.Form):
    file = forms.FileField(label="Select CSV file")

class MaintenanceImportForm(forms.Form):
    file = forms.FileField(label="Select CSV file")
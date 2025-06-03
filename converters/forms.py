from django import forms


OPERATION_CHOICES = [
    ('add', '+ Add'),
    ('subtract', '- Subtract'),
    ('multiply', '× Multiply'),
    ('divide', '÷ Divide'),
]

class FractionConversionForm(forms.Form):
    fraction1 = forms.CharField(
        label="First Fraction",
        widget=forms.TextInput(attrs={'placeholder': '3/4 or 1 1/2'}),
        help_text="Enter fractions as '3/4' or mixed numbers as '1 1/2'"
    )
    operation = forms.ChoiceField(
        choices=OPERATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    fraction2 = forms.CharField(
        label="Second Fraction",
        widget=forms.TextInput(attrs={'placeholder': '2/3 or 2 3/4'}),
        help_text="Enter fractions as '2/3' or mixed numbers as '2 3/4'"
    )


UNIT_CHOICES = [
    ('mm', 'Millimeters (mm)'),
    ('cm', 'Centimeters (cm)'),
    ('m', 'Meters (m)'),
    ('km', 'Kilometers (km)'),
    ('in', 'Inches (in)'),
    ('ft', 'Feet (ft)'),
    ('yd', 'Yards (yd)'),
    ('mi', 'Miles (mi)')
]

class LengthConversionForm(forms.Form):
    input_value = forms.FloatField(label="Value")
    from_unit = forms.ChoiceField(choices=UNIT_CHOICES, label="From")
    to_unit = forms.ChoiceField(choices=UNIT_CHOICES, label="To")

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from converters.forms import LengthConversionForm
from ..utils.length import convert_length

def length_converter(request):
    result = None
    calculation = None
    
    if request.method == 'POST':
        form = LengthConversionForm(request.POST)
        if form.is_valid():
            input_value = form.cleaned_data['input_value']
            from_unit = form.cleaned_data['from_unit']
            to_unit = form.cleaned_data['to_unit']
            
            result = convert_length(input_value, from_unit, to_unit)
            calculation = f"{input_value} {from_unit} = {result:.6f} {to_unit}"
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'result': result,
                    'calculation': calculation
                })
    else:
        form = LengthConversionForm()

    return render(request, 'converters/length.html', {
        'form': form,
        'result': result,
        'calculation': calculation
    })

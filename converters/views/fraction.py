from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from converters.forms import FractionConversionForm
from ..utils.fraction import convert_fraction

def fraction_converter(request):
    result = None
    error = None
    
    if request.method == 'POST':
        form = FractionConversionForm(request.POST)
        if form.is_valid():
            try:
                frac1 = form.cleaned_data['fraction1']
                frac2 = form.cleaned_data['fraction2']
                operation = form.cleaned_data['operation']
                
                result = convert_fraction(frac1, frac2, operation)
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({
                        'result': str(result),
                        'decimal': float(result)
                    })
            except ValueError as e:
                error = str(e)
    else:
        form = FractionConversionForm()

    return render(request, 'converters/fraction.html', {
        'form': form,
        'result': result,
        'error': error
    })
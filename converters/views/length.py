from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from converters.forms import LengthConversionForm
from ..utils.length import convert_length
from django.contrib.auth.decorators import login_required

@login_required
def length_converter(request):
    result = None
    error = None

    if request.method == 'POST':
        try:
            value = float(request.POST.get('value', 0))
            from_unit = request.POST.get('from_unit')
            to_unit = request.POST.get('to_unit')

            # Conversion logic
            if from_unit == 'in':
                base = value * 25.4  # inches to mm
            elif from_unit == 'mm':
                base = value
            elif from_unit == 'ft':
                base = value * 304.8  # feet to mm
            elif from_unit == 'm':
                base = value * 1000  # meters to mm
            else:
                error = 'Invalid from unit'
                base = None

            if base is not None:
                if to_unit == 'in':
                    result = base / 25.4
                elif to_unit == 'mm':
                    result = base
                elif to_unit == 'ft':
                    result = base / 304.8
                elif to_unit == 'm':
                    result = base / 1000
                else:
                    error = 'Invalid to unit'

        except (ValueError, TypeError):
            error = 'Invalid input value'

        # For AJAX, return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if error:
                return JsonResponse({'success': False, 'error': error})
            else:
                return JsonResponse({'success': True, 'result': result})

    return render(request, 'converters/length.html')
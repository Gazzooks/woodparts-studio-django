from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from fractions import Fraction

@login_required
def fraction_to_decimal_mm(request):
    # List of common fractions for the Fraction to Decimal & mm tab
    common_fractions = [
        {'numerator': 1, 'denominator': 16}, {'numerator': 1, 'denominator': 8}, {'numerator': 3, 'denominator': 16},
        {'numerator': 1, 'denominator': 4}, {'numerator': 5, 'denominator': 16}, {'numerator': 3, 'denominator': 8},
        {'numerator': 7, 'denominator': 16}, {'numerator': 1, 'denominator': 2}, {'numerator': 9, 'denominator': 16},
        {'numerator': 5, 'denominator': 8}, {'numerator': 11, 'denominator': 16}, {'numerator': 3, 'denominator': 4},
        {'numerator': 13, 'denominator': 16}, {'numerator': 7, 'denominator': 8}, {'numerator': 15, 'denominator': 16}
    ]

    # Handle AJAX POST request
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        try:
            # Get values from POST data
            whole = request.POST.get('whole', '').strip()
            numerator = request.POST.get('numerator', '').strip()
            denominator = request.POST.get('denominator', '').strip()

            # Validate input: if all fields are empty, return error
            if not whole and not numerator and not denominator:
                return JsonResponse({'error': 'Enter values to convert.'})

            # Convert to integers, use defaults if needed
            whole = int(whole) if whole else 0
            num = int(numerator) if numerator else 0
            denom = int(denominator) if denominator else 16

            # If user entered nothing meaningful, return error
            if whole == 0 and num == 0 and denom == 16:
                return JsonResponse({'error': 'Enter values to convert.'})

            # Do the conversion
            frac = Fraction(num, denom)
            decimal_inch = round(whole + float(frac), 4)
            millimeters = round(decimal_inch * 25.4, 3)

            return JsonResponse({
                'whole': whole,
                'numerator': num,
                'denominator': denom,
                'decimal_inch': decimal_inch,
                'millimeters': millimeters,
            })
        except Exception:
            return JsonResponse({'error': 'Invalid input.'})

    # On GET or non-AJAX POST, render the full page (initial load or fallback)
    return render(request, 'fraction_decimal_mm/fraction_to_decimal_mm.html', {
        'common_fractions': common_fractions,
        'active_tab': 'fraction_to_decimal_mm'
    })

@login_required
def decimal_to_fraction(request):
    results = {}
    if request.method == 'POST':
        try:
            decimal_inch = float(request.POST.get('decimal_inch', 0))
            precision = int(request.POST.get('precision', 16))
            whole = int(decimal_inch)
            frac = Fraction(decimal_inch - whole).limit_denominator(precision)
            if frac.numerator == 0:
                fractional = f"{whole}"
            elif whole == 0:
                fractional = f"{frac.numerator}/{frac.denominator}"
            else:
                fractional = f"{whole} {frac.numerator}/{frac.denominator}"
            millimeters = round(decimal_inch * 25.4, 3)
            results = {
                'decimal_inch': decimal_inch,
                'precision': str(precision),
                'fractional': fractional,
                'millimeters': millimeters
            }
        except Exception:
            results['error'] = "Invalid input."
    return render(request, 'fraction_decimal_mm/decimal_to_fraction.html', {
        'results': results,
        'active_tab': 'decimal_to_fraction'
    })

@login_required
def mm_to_fraction_decimal(request):
    results = {}
    if request.method == 'POST':
        try:
            millimeters = float(request.POST.get('millimeters', 0))
            precision = int(request.POST.get('precision', 16))
            decimal_inch = round(millimeters / 25.4, 4)
            whole = int(decimal_inch)
            frac = Fraction(decimal_inch - whole).limit_denominator(precision)
            if frac.numerator == 0:
                fractional = f"{whole}"
            elif whole == 0:
                fractional = f"{frac.numerator}/{frac.denominator}"
            else:
                fractional = f"{whole} {frac.numerator}/{frac.denominator}"
            results = {
                'millimeters': millimeters,
                'precision': str(precision),
                'decimal_inch': decimal_inch,
                'fractional': fractional
            }
        except Exception:
            results['error'] = "Invalid input."
    return render(request, 'fraction_decimal_mm/mm_to_fraction_decimal.html', {
        'results': results,
        'active_tab': 'mm_to_fraction_decimal'
    })

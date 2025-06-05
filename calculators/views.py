# calculators/views.py
"""
Calculators App - Handles various woodworking calculations

This module provides:
- Board foot calculator
- Fraction calculator
- Golden ratio calculator
- Shelf calculator
- Wall panels calculator
- Decking calculator
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from fractions import Fraction
import math

@login_required
def board_foot_calculator(request):
    user_prefers_metric = False
    if hasattr(request.user, 'userpreferences'):
        user_prefers_metric = (request.user.userpreferences.default_units == 'metric')

    result = None
    if request.method == 'POST':
        try:
            length = float(request.POST.get('length', 0))
            width = float(request.POST.get('width', 0))
            thickness = float(request.POST.get('thickness', 0))
            quantity = int(request.POST.get('quantity', 1))

            # Convert metric input to inches for calculation
            if user_prefers_metric:
                length = length / 25.4
                width = width / 25.4
                thickness = thickness / 25.4

            board_feet = (length * width * thickness / 144) * quantity
            result = round(board_feet, 2)
        except (ValueError, TypeError):
            result = None

    return render(request, 'calculators/board_foot.html', {
        'result': result,
        'user_prefers_metric': user_prefers_metric
    })



@login_required
def fraction_calculator(request):
    result = None
    decimal = None
    calculation = None
    error = None

    if request.method == 'POST':
        try:
            operation = request.POST.get('operation')
            frac1 = parse_fraction(request.POST.get('fraction1', ''))
            frac2 = parse_fraction(request.POST.get('fraction2', ''))

            if operation == 'add':
                res = add_fractions(frac1, frac2)
            elif operation == 'subtract':
                res = subtract_fractions(frac1, frac2)
            elif operation == 'multiply':
                res = multiply_fractions(frac1, frac2)
            elif operation == 'divide':
                res = divide_fractions(frac1, frac2)
            else:
                error = 'Invalid operation'
                res = None

            if res:
                simplified = simplify_fraction(res)
                result = format_fraction(simplified)
                decimal = float(simplified[0]) / float(simplified[1]) if simplified[1] != 0 else 0
                calculation = get_calculation_string(frac1, frac2, operation, simplified)
        except Exception as e:
            error = 'Invalid fraction format or calculation error'

        # If AJAX, return JSON
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            if error:
                return JsonResponse({'success': False, 'error': error})
            else:
                return JsonResponse({
                    'success': True,
                    'result': result,
                    'decimal': decimal,
                    'calculation': calculation
                })

    # For GET or non-AJAX POST, render the page as normal
    return render(request, 'calculators/fraction.html', {
        'result': result,
        'decimal': decimal,
        'calculation': calculation,
        'error': error
    })

# Helper functions for fraction calculations
def parse_fraction(fraction_str):
    """Parse fraction string into numerator/denominator tuple"""
    fraction_str = fraction_str.strip()
    
    if ' ' in fraction_str:
        whole, frac = fraction_str.split(' ', 1)
        whole = int(whole)
        if '/' in frac:
            num, den = map(int, frac.split('/'))
            return (whole * den + num, den)
        return (whole, 1)
    elif '/' in fraction_str:
        num, den = map(int, fraction_str.split('/'))
        return (num, den)
    elif fraction_str:
        return (int(fraction_str), 1)
    return (0, 1)

def add_fractions(frac1, frac2):
    """Add two fractions"""
    a, b = frac1
    c, d = frac2
    return (a*d + c*b, b*d)

def subtract_fractions(frac1, frac2):
    """Subtract two fractions"""
    a, b = frac1
    c, d = frac2
    return (a*d - c*b, b*d)

def multiply_fractions(frac1, frac2):
    """Multiply two fractions"""
    a, b = frac1
    c, d = frac2
    return (a*c, b*d)

def divide_fractions(frac1, frac2):
    """Divide two fractions"""
    a, b = frac1
    c, d = frac2
    return (a*d, b*c)

def gcd(a, b):
    """Greatest common divisor using Euclidean algorithm"""
    while b:
        a, b = b, a % b
    return a

def simplify_fraction(fraction):
    """Simplify fraction to lowest terms"""
    num, den = fraction
    common = gcd(abs(num), abs(den))
    return (num//common, den//common) if common != 0 else (0, 1)

def format_fraction(fraction):
    """Format fraction for display"""
    num, den = fraction
    if den == 1:
        return str(num)
    if abs(num) > den:
        whole = num // den
        remainder = abs(num) % den
        return f"{whole} {remainder}/{den}"
    return f"{num}/{den}"

def get_calculation_string(frac1, frac2, operation, result):
    """Generate human-readable calculation string"""
    ops = {
        'add': '+',
        'subtract': '-',
        'multiply': '×',
        'divide': '÷'
    }
    return (f"{format_fraction(frac1)} {ops[operation]} {format_fraction(frac2)} = " 
            f"{format_fraction(result)}")

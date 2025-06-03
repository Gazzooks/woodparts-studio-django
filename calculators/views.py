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
    """Board foot calculator - equivalent to desktop BoardFootCalculator"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            length = float(data.get('length', 0))
            width = float(data.get('width', 0))
            thickness = float(data.get('thickness', 0))
            quantity = int(data.get('quantity', 1))
            
            # Calculate board feet: (L × W × T × Qty) ÷ 144
            board_feet = (length * width * thickness * quantity) / 144
            
            # Calculate volume in cubic inches
            cubic_inches = length * width * thickness * quantity
            
            return JsonResponse({
                'success': True,
                'board_feet': round(board_feet, 4),
                'cubic_inches': cubic_inches,
                'calculation': f"{length}\" × {width}\" × {thickness}\" × {quantity} = {board_feet:.4f} BF",
                'formula': "Board Feet = (Length × Width × Thickness × Quantity) ÷ 144"
            })
        except (ValueError, TypeError) as e:
            return JsonResponse({
                'success': False,
                'error': 'Invalid input values. Please enter numbers only.'
            })
    
    return render(request, 'calculators/board_foot.html')

@login_required
def fraction_calculator(request):
    """Fraction calculator - equivalent to desktop FractionCalculator"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            operation = data.get('operation')
            frac1 = parse_fraction(data.get('fraction1', ''))
            frac2 = parse_fraction(data.get('fraction2', ''))
            
            if operation == 'add':
                result = add_fractions(frac1, frac2)
            elif operation == 'subtract':
                result = subtract_fractions(frac1, frac2)
            elif operation == 'multiply':
                result = multiply_fractions(frac1, frac2)
            elif operation == 'divide':
                result = divide_fractions(frac1, frac2)
            else:
                return JsonResponse({'success': False, 'error': 'Invalid operation'})
            
            simplified = simplify_fraction(result)
            return JsonResponse({
                'success': True,
                'result': format_fraction(simplified),
                'decimal': float(simplified[0]) / float(simplified[1]) if simplified[1] != 0 else 0,
                'calculation': get_calculation_string(frac1, frac2, operation, simplified)
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': 'Invalid fraction format or calculation error'
            })
    
    return render(request, 'calculators/fraction.html')

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

from fractions import Fraction

def parse_fraction(value):
    """Parse mixed numbers and fractions into Fraction objects"""
    if ' ' in value:
        whole, fraction = value.split(' ', 1)
        return Fraction(whole) + Fraction(fraction)
    return Fraction(value)

def convert_fraction(frac1, frac2, operation):
    """Perform fraction calculations with error handling"""
    try:
        f1 = parse_fraction(frac1)
        f2 = parse_fraction(frac2)
        
        if operation == 'add':
            return f1 + f2
        if operation == 'subtract':
            return f1 - f2
        if operation == 'multiply':
            return f1 * f2
        if operation == 'divide':
            return f1 / f2
        raise ValueError("Invalid operation")
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero")
    except:
        raise ValueError("Invalid fraction format")

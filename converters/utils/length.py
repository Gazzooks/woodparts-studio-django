CONVERSION_TABLE = {
    'mm': {'cm': 0.1, 'm': 0.001, 'km': 1e-6, 'in': 0.0393701, 'ft': 0.00328084, 'yd': 0.00109361, 'mi': 6.2137e-7},
    'cm': {'mm': 10, 'm': 0.01, 'km': 1e-5, 'in': 0.393701, 'ft': 0.0328084, 'yd': 0.0109361, 'mi': 6.2137e-6},
    'm': {'mm': 1000, 'cm': 100, 'km': 0.001, 'in': 39.3701, 'ft': 3.28084, 'yd': 1.09361, 'mi': 0.000621371},
    'km': {'mm': 1e6, 'cm': 1e5, 'm': 1000, 'in': 39370.1, 'ft': 3280.84, 'yd': 1093.61, 'mi': 0.621371},
    'in': {'mm': 25.4, 'cm': 2.54, 'm': 0.0254, 'km': 2.54e-5, 'ft': 0.0833333, 'yd': 0.0277778, 'mi': 1.5783e-5},
    'ft': {'mm': 304.8, 'cm': 30.48, 'm': 0.3048, 'km': 0.0003048, 'in': 12, 'yd': 0.333333, 'mi': 0.000189394},
    'yd': {'mm': 914.4, 'cm': 91.44, 'm': 0.9144, 'km': 0.0009144, 'in': 36, 'ft': 3, 'mi': 0.000568182},
    'mi': {'mm': 1.609e6, 'cm': 160934, 'm': 1609.34, 'km': 1.60934, 'in': 63360, 'ft': 5280, 'yd': 1760}
}

def convert_length(value, from_unit, to_unit):
    """Convert length between different units"""
    try:
        return value * CONVERSION_TABLE[from_unit][to_unit]
    except KeyError:
        raise ValueError("Invalid units provided")

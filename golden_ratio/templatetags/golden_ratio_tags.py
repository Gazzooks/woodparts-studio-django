from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return value

@register.filter
def max_value(value, arg):
    try:
        return max(float(value), float(arg))
    except (ValueError, TypeError):
        return value

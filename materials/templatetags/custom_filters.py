# materials/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def mul(value, arg):
    return float(value) * float(arg)

from django import template
import re

register = template.Library()

@register.filter
def intspace(value):
    """
    Converts an integer or float to a string containing spaces every three digits.
    For example: 234011889 becomes '234 011 889'.
    """
    try:
        if isinstance(value, str):
            value = value.replace(',', '').replace(' ', '').replace('\xa0', '')
        value = int(float(value))
    except (ValueError, TypeError):
        return value
        
    return '{:,}'.format(value).replace(',', ' ')

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def has_key(value, arg):
	return value.has_key(arg)


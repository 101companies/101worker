from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def back(value):
	return value[:value.rindex('/')]


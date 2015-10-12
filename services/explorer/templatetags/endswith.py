
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def endswith(value, arg):
	return value.endswith(arg)



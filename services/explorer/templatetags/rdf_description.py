from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def rdf_description(value):
	if value.endswith('/'):
		return value[:-1].replace(' ', '_') + '?format=rdf'
	else:
		return value.replace(' ', '_') + '?format=rdf'


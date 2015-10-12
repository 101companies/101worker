from django.http import HttpResponse
from models import lookup
import json
import os

def serveResourceNames(request, format):
    backlinks = os.path.join(os.path.dirname(__file__), 'backlinks.json')
    mappings = os.path.join(os.path.dirname(__file__), 'mapping.json')

    isJsonp = format == 'jsonp'
    
    resources = json.load(open(backlinks))['resources']
    result = json.dumps({'availableResouces' : resources})
    if isJsonp:
       result = request.GET.get('callback', 'callback') + '(' + result + ')'
    return HttpResponse(result, content_type='application/javascript' if isJsonp else 'text/json')

def serveTerm(request, format, term, resource=""):
    backlinks = os.path.join(os.path.dirname(__file__), 'backlinks.json')
    mappings = os.path.join(os.path.dirname(__file__), 'mapping.json')

    isJsonp = format == 'jsonp'
    
    backlinksInfo = json.load(open(backlinks))
    mapping = json.load(open(mappings))
    backlinks = backlinksInfo['backlinks']
    
    if resource:
        result = json.dumps(lookup(term,resource,mapping,backlinks))
    else:
        result = []
        resources = backlinksInfo['resources']
        for resource in resources:
            cResult = lookup(term,resource,mapping,backlinks)
            cResult['name'] = resource
            cResult['fullName'] = resources[resource]['fullName']
            cResult['isLinkable'] = resources[resource]['isLinkable']
            result.append(cResult)
        result = json.dumps(result)
    if isJsonp:
       result = request.GET.get('callback', 'callback') + '(' + result + ')'
    return HttpResponse(result, content_type='application/javascript' if isJsonp else 'text/json')



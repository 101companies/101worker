from django.http import HttpResponse
from models import lookup

def serveResourceNames(request, format):
    isJsonp = request.GET.get('format', '') == 'jsonp'
    
    resources = json.load(open('./backlinks.json'))['resources']
    result = json.dumps({'availableResouces' : resources})
    if isJsonp:
       result = params.get('callback', 'callback') + '(' + result + ')'
    return HttpResponse(result, content_type='application/javascript' if isJsonp else 'text/json')

def serveTerm(request, format, term, resource=""):
    isJsonp = request.GET.get('format', '') == 'jsonp'
    
    backlinksInfo = json.load(open('./backlinks.json'))
    mapping = json.load(open('./mapping.json'))
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
       result = params.get('callback', 'callback') + '(' + result + ')'
    return HttpResponse(result, content_type='application/javascript' if isJsonp else 'text/json')



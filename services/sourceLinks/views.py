import urllib2
import json
from django.http import Http404, HttpResponse

def serveLink(request, name, format):
    rawdata = urllib2.urlopen('http://data.101companies.org/dumps/PullRepo.json')
    data = json.load(rawdata)
    if name in data:
        result = [{'link': data[name], 'name': 'View code at GitHub'}]
        result.append({'link': "http://data.101companies.org/zips/contributions/" + name + ".zip", 'name': "Download .zip"})
        result = json.dumps(result)
        if format == 'jsonp':
            result = request.GET.get('callback', 'callback') + '(' + result + ')'
            content_type = 'application/javascript'
        else:
            content_type = 'text/json'
        return HttpResponse(result, content_type=content_type)
    else:
        raise Http404

def routes():
    return [
        ('/sourceLinks/(?P<name>.+)\.(?P<format>.+)', serveLink),
    ]

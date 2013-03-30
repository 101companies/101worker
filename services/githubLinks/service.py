import urllib2
import json

def serveLink(environ, start_response, params):
    name = params.get('name', '')
    rawdata = urllib2.open('http://localhost/dumps/PullRepo.jsonp')
    data = json.load(rawdata)
    if name in data:
        start_response('200 OK', response_headers)
        result = json.dumps(data[name])
        if iparams.get('format', '') and params.get('format', '') == 'jsonp':
            response_headers = [('Content-Type', 'text/jsonp')]
            result = 'resourcecallback(' + result + ')'
        else:
            response_headers = [('Content-Type', 'text/json')]
        return result
    else:
        start_response('404 Resource not found', [('Content-Type', 'text/plain')])

def routes():
    return [
        ('/githubLinks/(?P<name>.+)\.(?P<format>.+)', serveLink),
    ]

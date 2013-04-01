import urllib2
import json

def serveLink(environ, start_response, params):
    name = params.get('name', '')
    rawdata = urllib2.urlopen('http://data.101companies.org/dumps/PullRepo.json')
    data = json.load(rawdata)
    if name in data:
        result = [json.dumps({'link': data[name], 'name': 'Source at GitHub'})]
        result.append({'link': "http://data.101companies.org/zips/contributions/" + name + ".zip", 'name': "Download .zip"})
        if params.get('format', '') and params.get('format', '') == 'jsonp':
            response_headers = [('Content-Type', 'text/jsonp')]
            result = 'githublinkcallback(' + result + ')'
        else:
            response_headers = [('Content-Type', 'text/json')]
        start_response('200 OK', response_headers)
        return result
    else:
        start_response('404 Resource not found', [('Content-Type', 'text/plain')])

def routes():
    return [
        ('/githubLinks/(?P<name>.+)\.(?P<format>.+)', serveLink),
    ]

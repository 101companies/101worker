import json

def serveResourceNames(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/json')]
    start_response(status, response_headers)
    resourceNames = json.load(open('./backlinks.json'))['resources']
    return json.dumps({'availableResouces' : resourceNames})

def serveTerm(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/json')]
    start_response(status, response_headers)
    backlinks = json.load(open('./backlinks.json'))['backlinks']
    term = params.get('term', '')
    if term in backlinks:
        return json.dumps({'backlinks' : backlinks[term]})
    else:
        return json.dumps({'error' : "No backlinks found"})


def routes():
    return [
        ('/termResources', serveResourceNames),
        ('/termResources/(?P<term>.+)', serveTerm),
        ('/termResources/(?P<term>.+)/(?P<resources>.+)', serveTerm),
    ]

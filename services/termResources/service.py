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
    backlinksInfo = json.load(open('./backlinks.json'))
    backlinks = backlinksInfo['backlinks']
    resourceNames = backlinksInfo['resources']
    term = params.get('term', '')
    resource = params.get('resource', '')
    if term in backlinks:
        if resource:
            if resource in resourceNames:
                return json.dumps({'backlinks' : backlinks[term][resource]})
            else:
                return json.dumps({'error' : "Unknown resource " + '"' + resource + '"'})
        else:
            return json.dumps({'backlinks' : backlinks[term]})
    else:
        return json.dumps({'error' : "No backlinks found"})


def routes():
    return [
        ('/termResources/(?P<term>.+)/(?P<resources>.+)', serveTerm),
        ('/termResources/(?P<term>.+)', serveTerm),
        ('/termResources', serveResourceNames)
    ]

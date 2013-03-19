import json

def serveResourceNames(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/json')]
    start_response(status, response_headers)
    resourceNames = json.load(open('./backlinks.json'))['resources']
    return json.dumps({'availableResouces' : resourceNames})

def lookup(term, resource, mapping, backlinks):
    if resource in mapping:
        if term in mapping[resource]:
            if mapping[resource][term] in backlinks:
                return {'backlinks' : backlinks[mapping[resource][term]][resource]}
            else:
                return {'error' : "No backlinks found for " + term}
        else:
            return {'error' : "No mapping found for " + term}
    else:
        return {'error' : "Unknown resource " + '"' + resource + '"'}


def serveTerm(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/json')]
    start_response(status, response_headers)
    backlinksInfo = json.load(open('./backlinks.json'))
    mapping = json.load(open('./mapping.json'))
    backlinks = backlinksInfo['backlinks']
    term = params.get('term', '')
    resource = params.get('resource', '')
    if resource:
        return json.dumps(lookup(term,resource,mapping,backlinks))
    else:
        result = {}
        resourceNames = backlinksInfo['resources']
        for resource in resourceNames:
            result[resourceName] = json.dumps(lookup(term,resource,mapping,backlinks))
        return json.dumps(result)

def routes():
    return [
        ('/termResources/(?P<term>.+)/(?P<resource>.+)', serveTerm),
        ('/termResources/(?P<term>.+)', serveTerm),
        ('/termResources', serveResourceNames)
    ]

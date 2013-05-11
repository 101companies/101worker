import json

def serveResourceNames(environ, start_response, params):
    status = '200 OK'
    isJsonp = params.get('format', '') and params.get('format', '') == 'jsonp'
    if isJsonp:
       response_headers = [('Content-Type', 'text/javascript')]
    else:
        response_headers = [('Content-Type', 'text/javascript')]
    start_response(status, response_headers)
    resources = json.load(open('./backlinks.json'))['resources']
    result = json.dumps({'availableResouces' : resources})
    if isJsonp:
       result = 'resourcecallback(' + result + ')'
    return result


def lookup(term, resource, mapping, backlinks):
    if resource in mapping:
        if term in mapping[resource]:
            if mapping[resource][term] in backlinks:
                return backlinks[mapping[resource][term]][resource]
            else:
                return {'error' : "No backlinks found for " + mapping[resource][term]}
        else:
            return {'error' : "No mapping found for " + term}
    else:
        return {'error' : "Unknown resource " + '"' + resource + '"'}


def serveTerm(environ, start_response, params):
    status = '200 OK'
    isJsonp = params.get('format', '') and params.get('format', '') == 'jsonp'
    if isJsonp:
       response_headers = [('Content-Type', 'text/javascript')]
    else:
        response_headers = [('Content-Type', 'text/javascript')]
    start_response(status, response_headers)
    backlinksInfo = json.load(open('./backlinks.json'))
    mapping = json.load(open('./mapping.json'))
    backlinks = backlinksInfo['backlinks']
    term = params.get('term', '')
    resource = params.get('resource', '')
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
       result = 'resourcecallback(' + result + ')'
    return result

def routes():
    return [
        ('/termResources/(?P<term>.+)/(?P<resource>.+)\.(?P<format>.+)', serveTerm),
        ('/termResources/(?P<term>.+)\.(?P<format>.+)', serveTerm),
        ('/termResources\.(?P<format>.+)', serveResourceNames)
    ]

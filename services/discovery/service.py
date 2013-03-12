from wsgiref import handlers

#helper which does some stuff that's always needed
def initServeRequest(environ):
    import discovery
    #setting the base uri - either localhost for developing/debugging or the real 101companies.org/resources url
    discovery.base_uri = 'http://101companies.org/resources'

    if 'localhost' in environ.get('HTTP_HOST', ''):
        discovery.base_uri = 'http://' + environ.get('HTTP_HOST', '') + environ.get('SCRIPT_NAME', '') + '/discovery'


#helper methods for responding with an error, in JSON or in HTML
def respondError(start_response, error):
    status = '500 Internal Server Error'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return str(error)

def respondJSON(start_response, response):
    import json
    status = '200 OK'
    response_headers = [('Content-Type', 'text/json')]
    start_response(status, response_headers)

    return json.dumps(response)

def respondHTML(start_response, response, template):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)

    import discovery
    from templates import TemplateCache
    response['base_uri'] = discovery.base_uri.replace('/discovery','')
    template = TemplateCache.getTemplate(template)

    return str( template.render(response) )


#possible entry points
def serveFileFragment(environ, start_response, params):
    initServeRequest(environ)
    import discovery

    try:
        response = discovery.discoverFileFragment(params.get('namespace', ''), params.get('member', ''),
                                              params.get('path', ''), params.get('file', ''),params.get('fragment', ''))

        if params.get('format', 'json') == 'json': return respondJSON(start_response, response)
        return respondHTML(start_response,response,'fragment.html')

    except Exception, error:
        return respondError(start_response, error)

def serveMemberFile(environ, start_response, params):
    initServeRequest(environ)
    import discovery

    try:
        response = discovery.discoverMemberFile(params.get('namespace',''), params.get('member',''),
                                                params.get('path', ''), params.get('file', ''))

        if params.get('format', 'json') == 'json': return respondJSON(start_response, response)

        return respondHTML(start_response,response,'file.html')

    except Exception, error:
        return respondError(start_response, error)

def serveMemberPath(environ, start_response, params):
    initServeRequest(environ)
    import discovery

    try:
        response = discovery.discoverMemberPath(params.get('namespace', ''), params.get('member', ''),
                                                params.get('path', ''))

        if params.get('format', 'json') == 'json': return respondJSON(start_response, response)
        return respondHTML(start_response,response,'folder.html')

    except Exception, error:
        return respondError(start_response, error)


def serveNamespaceMember(environ, start_response, params):
    initServeRequest(environ)
    import discovery

    try:
        response = discovery.discoverNamespaceMember(params.get('namespace', ''), params.get('member', ''))

        if params.get('format', 'json') == 'json': return respondJSON(start_response, response)
        return respondHTML(start_response,response,'folder.html')

    except Exception, error:
        return respondError(start_response, error)

def serveNamespace(environ, start_response, params):
    initServeRequest(environ)
    import discovery

    try:
        response = discovery.discoverNamespace(params.get('namespace', ''))

        if params.get('format', 'json') == 'json': return respondJSON(start_response, response)
        return respondHTML(start_response,response,'folder.html')

    except Exception, error:
        return respondError(start_response, error)

def serveAllNamespaces(environ, start_response, params):
    initServeRequest(environ)
    import discovery

    try:
        response = discovery.discoverAllNamespaces()

        if params.get('format', 'json') == 'json': return respondJSON(start_response, response)
        return respondHTML(start_response,response,'folder.html')

    except Exception, error:
        return respondError(start_response, error)

def routes():
    return [
        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)/(?P<path>.+)/(?P<file>.*\.[^/]+)/(?P<fragment>.+)', serveFileFragment),
        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)/(?P<path>.+)/(?P<file>.*\.[^/]+)', serveMemberFile),
        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)/(?P<path>.+)', serveMemberPath),
        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)', serveNamespaceMember),
        ( '/discovery/(?P<namespace>[^/]+)', serveNamespace),
        ( '/discovery', serveAllNamespaces )
    ]
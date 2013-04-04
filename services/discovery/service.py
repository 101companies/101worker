from wsgiref import handlers

#helper which does some stuff that's always needed
def initServeRequest(environ):
    import discovery
    #setting the base uri - either localhost for developing/debugging or the real 101companies.org/resources url
    discovery.base_uri = 'http://101companies.org/resources'

    if 'localhost' in environ.get('HTTP_HOST', ''):
        discovery.base_uri = 'http://' + environ.get('HTTP_HOST', '') + environ.get('SCRIPT_NAME', '') + '/discovery'


#helper methods for responding with an error, in JSON, HTML or RDF
def respondError(start_response, error):
    from discovery import DiscoveryException
    response_headers = [('Content-Type', 'text/plain')]

    if isinstance(error, DiscoveryException):
        start_response(error.Status, response_headers)
    else:
        start_response('500 Internal Server Error', response_headers)
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


    if 'content' in response:
        from xml.sax.saxutils import escape
        response['content'] = escape(response['content'])

    import discovery
    from templates import TemplateProvider
    #base URI, needed for static urls
    if 'localhost' in discovery.base_uri: response['base_uri'] = discovery.base_uri.replace('/discovery','')
    else: response['base_uri'] = 'http://worker.101companies.org/services'
    template = TemplateProvider.getTemplate(template)

    return str( template.render(response) )

def respondRDF(start_response, response, template, environ):
    response['about'] = 'http://101companies.org/resources' + environ['PATH_INFO'].replace('/discovery','')

    status = '200 OK'
    response_headers = [('Content-Type', 'application/rdf+xml')]
    start_response(status, response_headers)

    from templates import TemplateProvider
    template = TemplateProvider.getTemplate(template)

    return str( template.render(response) )


#possible entry points
def serveFileFragment(environ, start_response, params):
    initServeRequest(environ)
    import discovery

    try:
        if not params.get('path',None): params['path'] = ''

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
        #I don't understand under which circumstances the regex says that params['path'] = None, but it says it
        #in some cases => for these cases, the line is necessary
        if not params.get('path',None): params['path'] = ''

        response = discovery.discoverMemberFile(params.get('namespace',''), params.get('member',''),
                                                params.get('path', ''), params.get('file', ''))

        if params.get('format', 'json') == 'json': return respondJSON(start_response, response)
        if params['format'] == 'rdf': return respondRDF(start_response, response, 'file.rdf', environ)

        return respondHTML(start_response,response,'file.html')

    except Exception, error:
        return respondError(start_response, error)

def serveMemberPath(environ, start_response, params):
    initServeRequest(environ)
    import discovery
    from data101 import DumpdataProvider
    import os

    #needed for strange files, that have no . ! e.g. "Makefile"
    #This is also the reason why serveMemberPath doesn't need a check if a path exists, because non existing paths will
    #be classified as files first!!!
    if not DumpdataProvider.isDir(os.path.join(params.get('namespace',''), params.get('member',''),params.get('path',''))):
        path = params['path']
        params['path'] = os.path.dirname(path)
        params['file'] = os.path.basename(path)
        return serveMemberFile(environ, start_response, params)

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

        return respondHTML(start_response,response,'namespace.html')

    except Exception, error:
        return respondError(start_response, error)

def serveAllNamespaces(environ, start_response, params):
    initServeRequest(environ)
    import discovery

    try:
        response = discovery.discoverAllNamespaces()

        if params.get('format', 'json') == 'rdf': return respondRDF(start_response, response, 'namespace.rdf', environ)
        if params.get('format', 'json') == 'json': return respondJSON(start_response, response)
        return respondHTML(start_response,response,'namespace.html')

    except Exception, error:
        return respondError(start_response, error)

def routes():
    return [
        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)(/(?P<path>.*))?/(?P<file>.*\.[^/]+)/(?P<fragment>.+)', serveFileFragment),
        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)(/(?P<path>.*))?/(?P<file>.*\.[^/]+)', serveMemberFile),
        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)/(?P<path>.+)', serveMemberPath),
        ( '/discovery/(?P<namespace>[^/]+)/(?P<member>[^/]+)', serveNamespaceMember),
        ( '/discovery/(?P<namespace>[^/]+)', serveNamespace),
        ( '/discovery', serveAllNamespaces )
    ]
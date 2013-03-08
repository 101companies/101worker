def initServeRequest(environ):
    import re
    import discovery
    #setting the base uri - either localhost for developing/debugging or the real 101companies.org/resources url
    discovery.base_uri = 'http://101companies.org/resources'

    if 'localhost' in environ.get('HTTP_HOST', ''):
        discovery.base_uri = 'http://' + environ.get('HTTP_HOST', '') + environ.get('SCRIPT_NAME', '') + '/discovery'
    if environ['QUERY_STRING']:
        return dict(re.findall(r'(\S+)=(".*?"|\S+)', environ['QUERY_STRING']))

    return {}

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

    from jinja2 import Template
    template = Template(''.join(open(template, 'r').readlines()))
    return str(template.render(response))

def noParam(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    response_body = 'DiscoveryService: Please specify some parameters'
    start_response(status, response_headers)
    return response_body

def serveDirRequest(environ, start_response, params):
    url_params = initServeRequest(environ)
    import discovery

    try:
        response = discovery.discoverDir(params.get('filePath', ''))
        if url_params.get('format', 'json') == 'json': return respondJSON(start_response, response)

        return respondHTML(start_response,response,'templates/discoverDir.html')

    except Exception, error:
        return respondError(start_response, error)

def serveFileRequest(environ, start_response, params):
    url_params = initServeRequest(environ)
    import discovery

    try:
        response = discovery.discoverFile(params.get('filePath', ''), params.get('fileName', ''))
        if url_params.get('format', 'json') == 'json': return respondJSON(start_response, response)

        return respondHTML(start_response,response,'templates/discoverFile.html')

    except Exception, error:
        return respondError(start_response, error)

def serveFragmentRequest(environ, start_response, params):
    url_params = initServeRequest(environ)
    import discovery

    try:
        response = discovery.discoverFragment(params.get('filePath', ''), params.get('fileName', ''), params.get('fragment', ''))
        if url_params.get('format', 'json') == 'json': return respondJSON(start_response, response)

        return respondHTML(start_response,response,'templates/discoverFragment.html')

    except Exception, error:
        return respondError(start_response, error)

def routes():
    return [
        ( '/discovery/(?P<filePath>.+)/(?P<fileName>.*\.[^/]+)/(?P<fragment>.+)', serveFragmentRequest ),
        ( '/discovery/(?P<filePath>.+)/(?P<fileName>.*\.[^/]+)', serveFileRequest ),
        ( '/discovery/(?P<filePath>.+)/Makefile', serveFileRequest ),
        ( '/discovery/(?P<filePath>.+)(/)?', serveDirRequest ),
        ( '/discovery', serveDirRequest )
    ]
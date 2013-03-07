def noParam(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    response_body = 'DiscoveryService: Please specify some parameters'
    start_response(status, response_headers)
    return response_body

def serveRequest(environ, start_response, params):
    import discovery
    import re

    try:
        #setting url params, if there are any
        url_params = {}
        if environ['QUERY_STRING']:
            url_params = dict(re.findall(r'(\S+)=(".*?"|\S+)', environ['QUERY_STRING']))

        #setting the base uri - either localhost for developing/debugging or the real 101companies.org/resources url
        discovery.base_uri = 'http://101companies.org/resources'
        if 'localhost' in environ.get('HTTP_HOST', ''):
            discovery.base_uri = 'http://' + environ.get('HTTP_HOST', '') + environ.get('SCRIPT_NAME', '') + '/discovery'

        if 'fileName' in params and 'fragment' in params:
            templateFile = 'templates/discoverFragment.html'
            response = discovery.discoverFragment(params['filePath'], params['fileName'], params['fragment'])
        elif 'fileName' in params:
            templateFile = 'templates/discoverFile.html'
            response = discovery.discoverFile(params['filePath'], params['fileName'])
        else:
            templateFile = 'templates/discoverDir.html'
            response = discovery.discoverDir(params['filePath'])

        #standard case is that we return json
        if 'json' == url_params.get('format', 'json'):
            import json
            status = '200 OK'
            response_headers = [('Content-Type', 'text/json')]
            start_response(status, response_headers)
            return json.dumps(response)

        status = '200 OK'
        response_headers = [('Content-Type', 'text/html')]
        start_response(status, response_headers)

        from jinja2 import Template
        template = Template(''.join(open(templateFile, 'r').readlines()))
        return str(template.render(response))

    except Exception, error:
        status = '500 Internal Server Error'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return str(error)

def routes():
    return [
        ( '/discovery/(?P<filePath>.+)/(?P<fileName>.*\.[^/]+)/(?P<fragment>.+)', serveRequest ),
        ( '/discovery/(?P<filePath>.+)/(?P<fileName>.*\.[^/]+)', serveRequest ),
        ( '/discovery/(?P<filePath>.+)(/)?', serveRequest ),
        ( '/discovery', noParam )
    ]
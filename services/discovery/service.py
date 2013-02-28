def noParam(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    response_body = 'DiscoveryService: Please specify some parameters'
    start_response(status, response_headers)
    return response_body

def serveRequest(environ, start_response, params):
    import discovery

    try:
        status = '200 OK'
        response_headers = [('Content-Type', 'text/json')]
        start_response(status, response_headers)

        discovery.base_uri = environ.get('HTTP_HOST', '') + environ.get('SCRIPT_NAME', '') + '/discovery'

        if 'fileName' in params and 'fragment' in params:
            return discovery.discoverFragment(params['filePath'], params['fileName'], params['fragment'])
        if 'fileName' in params:
            return discovery.discoverFile(params['filePath'], params['fileName'])

        return discovery.discoverDir(params['filePath'])
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

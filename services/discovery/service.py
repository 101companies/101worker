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
        url_params = {}
        if environ['QUERY_STRING']:
            url_params = dict(re.findall(r'(\S+)=(".*?"|\S+)', environ['QUERY_STRING']))

        if 'localhost' in environ.get('HTTP_HOST', ''):
            discovery.base_uri = 'http://' + environ.get('HTTP_HOST', '') + environ.get('SCRIPT_NAME', '') + '/discovery'
        else:
            discovery.base_uri = 'http://101companies.org/resources'

        if 'fileName' in params and 'fragment' in params:
            response = discovery.discoverFragment(params['filePath'], params['fileName'], params['fragment'])
        elif 'fileName' in params:
            response = discovery.discoverFile(params['filePath'], params['fileName'])
        else:
            response = discovery.discoverDir(params['filePath'])

        if 'html' == url_params.get('format', 'json'):
            return _htmlResponse(start_response, response)

        return _jsonResponse(start_response, response)

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


def _jsonResponse(start_response, response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/json')]
    start_response(status, response_headers)

    import json
    return json.dumps(response)

def _htmlResponse(start_response, response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html')]
    start_response(status, response_headers)

    return _wrapInHTML(response)

def _wrapInHTML(response):
    from string import Template
    def read(path):
        return ''.join(open(path, 'r').readlines())

    if 'folders' in response:
        dirTemplate = Template(read('templates/discoverDir.html'))

        dirs = ''
        for d in response['folders']:
            dirs += Template(read('templates/singledir.html')).substitute({'name':str(d['name']), 'link':str(d['resource'])})
        if dirs == '': dirs = 'None'

        files = ''
        for f in response['files']:
            files += Template(read('templates/singlefile.html')).substitute({'name':str(f['name']), 'link':str(f['resource'])})
        if files == '': files = 'None'

        return dirTemplate.substitute({'folderList' : dirs, 'filesList' : files})

    #if it isn't a folder, then we can expect some values
    if 'fragments' in response:
        fragments = ''
        for f in response['fragments']:
            fragments += Template(read('templates/singlefragment.html')).substitute({'name':str(f['name']), 'link':str(f['resource'])})
        if fragments == '': fragments = 'None'
    else:
        fragments = 'not extractable'

    if 'content' in response:
        content = response['content']
    else:
        content = 'not extractable'


    if 'github' in response:
        fileTemplate = Template(read('templates/discoverFile.html'))
        return fileTemplate.substitute({'content': content, 'fragmentList':fragments, 'github':str(response['github'])})


    fragmentTemplate = Template(read('templates/discoverFragment.html'))
    return fragmentTemplate.substitute({'content': content, 'fragmentList': fragments, 'fragmentType': str(response['classifier'])})

def match(environ, start_response, params):
    import matches
    import json

    results = matches.matchFiles(params.get('username', ''), params.get('reponame', ''), params.get('subfolder', ''))

    if results == None:
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return 'Not found'


    status = '200 OK'
    response_headers = [('Content-Type', 'text/json')]
    start_response(status, response_headers)

    return json.dumps(results)




def routes():
    return [
        ('/matches/(?P<username>[^/]+)/(?P<reponame>[^/]+)(/)?(?P<subfolder>.*)', match),
    ]
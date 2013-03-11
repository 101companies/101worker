def helloName(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)

    return 'Hello ' + params['name'] + ', how are you?'


def hello(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)

    return 'Hello World'


def routes():
    return [
        ('/termResources/(?P<name>[^/]+)', helloName),
        ('/termResources', hello)
    ]

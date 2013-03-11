def helloName(environ, start_response, params):
    try:
        status = '200 OK'
        response_headers = [('Content-Type', 'text/json')]
        start_response(status, response_headers)
        return {}
    except Exception as e:
         return respondError(start_response, error)


def hello(environ, start_response, params):
    try:
        status = '200 OK'
        response_headers = [('Content-Type', 'text/json')]
        start_response(status, response_headers)
        return {}
    except Exception as e:
         return respondError(start_response, error)

def respondError(start_response, error):
    status = '500 Internal Server Error'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return str(error)

def routes():
    return [
        ('/termResources/(?P<name>[^/]+)', helloName),
        ('/termResources', hello)
    ]

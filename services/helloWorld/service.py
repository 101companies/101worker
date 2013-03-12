import json

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

def debugVariables(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type','text/json')]
    start_response(status,response_headers)

    response = {}
    response['keys'] = environ.keys()
    response['wsgi.run_once'] = environ['wsgi.run_once']
    response['wsgi.multiprocess'] = environ['wsgi.multiprocess']
    response['wsgi.multithread'] = environ['wsgi.multithread']
    return json.dumps(response)


def routes():
    return [
        ('/hello/(?P<name>[^/]+)', helloName),
        ('/hello', hello),
        ('/debug',debugVariables)
    ]
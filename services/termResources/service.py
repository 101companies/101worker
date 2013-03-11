import json

def serveResourceNames(environ, start_response, params):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/json')]
    start_response(status, response_headers)
    resourceNames = json.load(open('./resources.json'))['resources']
    return json.dumps({'availableResouces' : resourceNames})

def routes():
    return [
        ('/termResources', serveResourceNames)
    ]

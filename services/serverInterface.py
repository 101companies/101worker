#! /usr/bin/env python

import sys
import os
import re
import imp

textExtensions = ('.css', '.js')
mimeTypes = {
    '.css': 'text/css',
    '.js' : 'text/javascript'
}

#handle static file calls
def handleText(environ, start_response,ext):
    start_response("200 Ok", [
        ('Content-Type', mimeTypes[ext]),
        ('Cache-Control','max-age=3600, must-revalidate'),
        ('Expires',' Fri, 30 Oct 1998 14:19:41 GMT'),
        ('Last-Modified','Last-Modified: Mon, 29 Jun 1998 02:28:12 GMT')
    ])
    response_body = ''.join(open(os.path.join(os.path.dirname(__file__),environ['PATH_INFO'][1:]),'r').readlines())
    return response_body

#dynamic stuff
def loadScripts():
    routes = []
    for (root, dirs, files) in os.walk(os.path.dirname(__file__)):
        for file in files:
            if file == 'service.py':
                s = imp.load_source('service', os.path.join(root, file))
                for (pattern, callback) in s.routes():
                    c = re.compile(pattern)
                    routes.append((c, root, callback))
    return routes


def checkRoutes(environ, start_response, routes):
    path = environ.get('PATH_INFO', '')
    for (route, root, callback) in routes:
        m = route.match(path)
        if m:
            os.chdir(root)
            sys.path.append(os.getcwd())
            params = m.groupdict()
            if environ['QUERY_STRING']:
                params.update(dict(re.findall(r'(\S+)=(".*?"|\S+)', environ['QUERY_STRING'])))
            return callback(environ, start_response, params)

    start_response("404 Not Found", [('Content-Type', 'text/plain')])
    response_body = "Didn't find a service for this URL"
    return response_body

#entrypoint
def application(environ, start_response):
    try:
        #TODO I don't like that - I guess some discussion about the best way to deliver static files is necessary
        #check if a static (css, javascript, ...) is enough
        if environ.get('PATH_INFO','').startswith('/static'):
            if environ['PATH_INFO'].endswith(textExtensions):
                fileName, fileExt = os.path.splitext(environ['PATH_INFO'])
                return handleText(environ,start_response,fileExt)


        r = loadScripts()
        result = checkRoutes(environ, start_response, r)
        return [result]
    except Exception as e:
        start_response("500 Internal Server Error", [('Content-Type', 'text/plain')])
        str = 'Internal Server Error:\n'
        str += e.message
        str += '\nworking directory: ' + os.getcwd()
        return [str]

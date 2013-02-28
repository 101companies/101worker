#! /usr/bin/env python

import sys
import os
import re
import imp


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
            return callback(environ, start_response, m.groupdict())

    start_response("404 Not Found", [('Content-Type', 'text/plain')])
    response_body = "Didn't find a service for this URL"
    return response_body

#entrypoint
def application(environ, start_response):
    try:
        r = loadScripts()
        result = checkRoutes(environ, start_response, r)
        return [result]
    except Exception as e:
        start_response("500 Internal Server Error", [('Content-Type', 'text/plain')])
        str = 'Internal Server Error:\n'
        str += e.message
        str += '\nworking directory: ' + os.getcwd()
        return [str]

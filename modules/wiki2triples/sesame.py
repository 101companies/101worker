__author__ = 'Martin Leinberger'

import os
import httplib2


def clear_graph(uri):
    endpoint = os.path.join(uri, 'statements')
    data = "update=CLEAR ALL"
    (response, content) = httplib2.Http().request(endpoint, 'POST', body=data,
                                                  headers={ 'content-type': 'application/x-www-form-urlencoded',
                                                            'accept': 'application/sparql-update'})
    return response, content
    #assert response['status'] == '204'


def upload(uri, path):
    endpoint = os.path.join(uri, 'statements')
    data = open(path, 'r').read()
    (response, content) = httplib2.Http().request(endpoint, 'PUT', body=data, headers={ 'content-type': 'application/rdf+xml' })
    return response, content
    #print 'Response was {}'.format(response)

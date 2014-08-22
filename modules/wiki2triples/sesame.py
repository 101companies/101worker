__author__ = 'Martin'

import os
import httplib2
import urllib

def clear_graph(uri):
    endpoint = os.path.join(uri, 'statements')
    data = "update=CLEAR ALL"
    (response, content) = httplib2.Http().request(endpoint, 'POST', body=data,
                                                  headers={ 'content-type': 'application/x-www-form-urlencoded',
                                                            'accept': 'application/sparql-update'})
    response, content
    #assert response['status'] == '204'


def upload(uri, path):
    endpoint = "http://triples.101companies.org/openrdf-sesame/repositories/Testing_2/statements"
    data = open(path, 'r').read()
    (response, content) = httplib2.Http().request(endpoint, 'PUT', body=data, headers={ 'content-type': 'application/rdf+xml' })
    response, content
    #print 'Response was {}'.format(response)

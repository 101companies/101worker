# -*- coding: utf-8 -*-


import json
import os
import sys
sys.path.append('../../libraries')
from mediawiki import Sesame

def getTriplesContaining(namespace, member):
    query = '''
        SELECT *
        WHERE {
            { ?subject ?predicate <http://101companies.org/resource/%s-3A%s> } UNION { <http://101companies.org/resource/%s-3A%s> ?predicate ?object }
        }
	''' % (namespace, member, namespace, member)

    tripleStore = Sesame.Store()
    return tripleStore.select(query).get('results', {}).get('bindings', None)

#that concept doesn't have a namespace isn't a nice thing, because when someone wants "Namespace:Concept" I have to
#react differently than when someone wants the concept "Monoid"
def getEndpointLink(namespace, member):
    if member == '':
        member += 'Concept'
    if not namespace or namespace == '':
        return "http://101companies.org/endpoint/{}/json".format(member)
    else:
        return "http://101companies.org/endpoint/{0}:{1}/json".format(namespace, member)

def getSesameLink(namespace, member):
    #if member == '':
    #    member = 'Concept'
    return 'http://triples.101companies.org/openrdf-workbench/repositories/wiki2/explore?resource=%3Chttp%3A%2F%2F101companies.org%2Fresources%2F{}%2F{}%3E'.format(namespace, member)

    #if not namespace or namespace == '':
    #    return "http://triples.101companies.org/openrdf-workbench/repositories/wiki101/explore?resource=%3Chttp%3A%2F%2F101companies.org%2Fresource%2F{}%3E".format(member)
    #else:
    #    return "http://triples.101companies.org/openrdf-workbench/repositories/wiki101/explore?resource=%3Chttp%3A%2F%2F101companies.org%2Fresource%2F{0}-3A{1}%3E".format(namespace, member)
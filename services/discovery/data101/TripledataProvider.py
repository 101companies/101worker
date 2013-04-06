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
        member = 'Concept'
    if not namespace or namespace == '':
        return "http://sl-mac.uni-koblenz.de:8081/org.softlang.semanticendpoint/doQuery?method=getResourceTriples&resource={}".format(member)
    else:
        return "http://sl-mac.uni-koblenz.de:8081/org.softlang.semanticendpoint/doQuery?method=getResourceTriples&resource={0}-3A{1}".format(namespace, member)

def getSesameLink(namespace, member):
    if member == '':
        member = 'Concept'
    if not namespace or namespace == '':
        return "http://sl-mac.uni-koblenz.de:8081/openrdf-workbench/repositories/wiki101/explore?resource=wiki%3A{}".format(member)
    else:
        return "http://sl-mac.uni-koblenz.de:8081/openrdf-workbench/repositories/wiki101/explore?resource=wiki%3A{0}-3A{1}".format(namespace, member)
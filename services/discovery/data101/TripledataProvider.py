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

def getEndpointLink(namespace, member):
    return "http://sl-mac.uni-koblenz.de:8081/org.softlang.semanticendpoint/doQuery?method=getResourceTriples&resource={0}-3A{1}".format(namespace, member)

def getSesameLink(namespace, member):
    return "http://sl-mac.uni-koblenz.de:8081/openrdf-workbench/repositories/wiki101/explore?resource=wiki%3A{0}-3A{1}".format(namespace, member)
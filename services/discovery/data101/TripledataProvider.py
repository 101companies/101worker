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
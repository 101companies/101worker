#! /usr/bin/env python

import sys
import rdflib
import urllib
import httplib2
from pysesame import pySesame

sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')

from metamodel import Dumps


def refine(str):
    return str.strip().replace(' ', '_')


wiki = Dumps.WikiDump()

#general namespaces
rdfNs = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
emptyNS = rdflib.Namespace('')

#101companies specific namespaces
propertiesNS = rdflib.Namespace('http://101companies.org/property/')
resourcesNS = rdflib.Namespace('http://101companies.org/')
classesNs = rdflib.Namespace('http://101companies.org/schemas/wiki#')


graph = rdflib.Graph()

for page in wiki:
    subject = resourcesNS[ refine(page['p'] + ':' + page['n']) ]

    #adding classes
    for instance in page.get('instanceOf', []):
        if instance['n']:
            graph.add( (subject, rdfNs['type'], classesNs[instance['n']]))

    for link in page.get('internal_links', []):
        if '::' in link and link.count('::') == 1:
            predicate, object = link.split('::')
            predicate, object = refine(predicate[0].lower() + predicate[1:]), refine(object)
            predicate = propertiesNS[predicate.replace(':', '-')]
            if 'http://' in object:
                if '.wikipedia.org' in object:
                    #rewrite it to dbpedia
                    object = object.replace('http://en.wikipedia.org/wiki/', 'http://dbpedia.org/page/')
                object = emptyNS[object]
            else:
                object = resourcesNS[object]

            graph.add( (subject, predicate, object) )

subject, predicate, object = resourcesNS['Language:ANTLR.Notation'], propertiesNS['PartOf'], resourcesNS['Technology:ANTLR']
graph.add( (subject, predicate, object) )
subject, predicate, object = resourcesNS['Technology:ANTLR.Generator'], propertiesNS['PartOf'], resourcesNS['Technology:ANTLR']
graph.add( (subject, predicate, object) )

open('wikiLinks.rdf', 'w').write(graph.serialize())

print "Wrote wikiLinks.rdf"

repository = 'wiki2'#'ML_testing'
graph      = 'http://101companies.org'
filename   = 'wikiLinks.rdf'
params     = { 'context': '<' + graph + '>' }

#(response, content) = httplib2.Http().request('http://141.26.71.114/openrdf-sesame/repositories/ML_testing/clearRepository')
#print response, content

print "Trying to loading %s into %s in Sesame" % (filename, graph)
endpoint = "http://141.26.71.114/openrdf-sesame/repositories/%s/statements?%s" % (repository, urllib.urlencode(params))
data = open(filename, 'r').read()
(response, content) = httplib2.Http().request(endpoint, 'PUT', body=data, headers={ 'content-type': 'application/rdf+xml' })

if response.status == 204:
    print "Success"
else:
    print "ERROR - Response %s" % response.status
    print content
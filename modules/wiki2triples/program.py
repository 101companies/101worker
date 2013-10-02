#! /usr/bin/env python

import sys
import rdflib

sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')

from metamodel import Dumps


def refine(str):
    return str.strip().replace(' ', '_')


wiki = Dumps.WikiDump()

propsNS = rdflib.Namespace('http://101companies.org/property/')
resNS = rdflib.Namespace('http://101companies.org/')
emptyNS = rdflib.Namespace('')
graph = rdflib.Graph()

for page in wiki:
    subject = propsNS[ refine(page['p'] + ':' + page['n']) ]
    for link in page.get('internal_links', []):
        if '::' in link and link.count('::') == 1:
            predicate, object = link.split('::')
            predicate, object = refine(predicate), refine(object)
            predicate = propsNS[predicate.replace(':', '-')]
            if 'http://' in object:
                object = emptyNS[object]
            else:
                object = resNS[object]

            graph.add( (subject, predicate, object) )

open('wikiLinks.rdf', 'w').write(graph.serialize())

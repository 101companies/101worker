#! /usr/bin/env python

import sys
import rdflib

sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')

from metamodel import Dumps



def tempHelp(page):
    for instance in page['instanceOf']:
        if instance['p'] == 'Namespace':
            return instance['n']


wiki = Dumps.WikiDump()

props = rdflib.Namespace('http://101companies.org/property/')
res = rdflib.Namespace('http://101companies.org/resources/')
emptyNs = rdflib.Namespace('')
graph = rdflib.Graph()

for page in wiki:
    if page.get('instanceOf', None):
        subject = page['p']
        if tempHelp(page):
            subject = tempHelp(page) + ':' + subject
        for link in page.get('internal_links', []):
            if '::' in link and link.count('::') == 1:
                predicate, object = link.split('::')
                subject, predicate, object = subject.strip().replace(' ', '_'), predicate.strip().replace(' ', '_'), object.replace(' ', '_')
                #adding namespaces
                subject, predicate = res[subject], props[predicate]
                if not 'http://' in object:
                    object = res[object]
                else:
                    object = emptyNs[object]

                graph.add( (subject, predicate, object) )

print graph.serialize(format='n3')

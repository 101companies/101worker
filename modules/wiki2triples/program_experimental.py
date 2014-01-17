# -*- coding: utf-8 -*-
__author__ = 'Martin Leinberger'

import sys
sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')
import urllib


from metamodel.Dumps import WikiDump
from tools101 import tick

from rdflib import Namespace
from rdfalchemy.sparql.sesame2 import SesameGraph


rdf = Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
prop = Namespace('http://101companies.org/property/')
resources = Namespace('http://101companies.org/')
classes = Namespace('http://101companies.org/schemas/wiki#')
empty = Namespace('')

db = SesameGraph('http://triples.101companies.org/openrdf-sesame/repositories/ML_testing')


def refine(str):
    quoted = urllib.quote(str.strip().replace(' ', '_').encode('utf-8'))
    return quoted

# Clear the database
# TODO implement

if __name__ == "__main__":
    for page in WikiDump():
        tick()
        sub = refine(page['p']) + ':' + refine(page['n'])
        sub = resources[ sub ]

        links = filter(lambda x: '::' in x and x.count('::') == 1, page.get('internal_links', []))
        for link in links:
            pre, obj = link.split('::')
            pre, obj = prop[ refine(pre[0].lower() + pre[1:]).replace(':','-') ], refine(obj)

            if 'http://en.wikipedia.org/wiki/' in obj:
                obj = empty[ obj.replace('http://en.wikipedia.org/wiki/', 'http://dbpedia.org/page/') ]
            elif 'http://' in obj:
                obj = empty[ obj ]
            else:
                obj = resources[ obj ]

            db.add((sub, pre, obj))

    sub, pre, obj = resources['Language:ANTLR.Notation'], prop['PartOf'], resources['Technology:ANTLR']
    db.add( (sub, pre, obj) )

    sub, pre, obj = resources['Technology:ANTLR.Generator'], prop['PartOf'], resources['Technology:ANTLR']
    db.add( (sub, pre, obj) )
#! /usr/bin/env python


import rdflib


g = rdflib.Graph()
g.load('http://101companies.org/resources?format=rdf')
g += rdflib.Graph().parse('course.rdf')
#g += Graph().parse('concepts.nt', format='nt')
#g += Graph().parse('contributions.nt', format='nt')
#g += Graph().parse('features.nt', format='nt')
g += rdflib.Graph().parse('information.rdf')
g += rdflib.Graph().parse('languages.rdf')
g += rdflib.Graph().parse('oneOhOne.rdf')
g += rdflib.Graph().parse('properties.rdf')
g += rdflib.Graph().parse('resources.rdf')
g += rdflib.Graph().parse('scripts.rdf' )
#g += Graph().parse('services.nt', format='nt')
#g += Graph().parse('technologies.nt', format='nt')

open('complete.nt', 'w').write(g.serialize(format='nt'))
open('complete.rdf', 'w').write(g.serialize())


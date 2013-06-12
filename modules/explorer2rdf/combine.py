#! /usr/bin/env python


from rdflib.Graph import Graph


g = Graph()
g.load('http://101companies.org/resources?format=rdf')
g += Graph().parse('course.rdf')
#g += Graph().parse('concepts.nt', format='nt')
#g += Graph().parse('contributions.nt', format='nt')
#g += Graph().parse('features.nt', format='nt')
g += Graph().parse('information.rdf')
g += Graph().parse('languages.rdf')
g += Graph().parse('oneOhOne.rdf')
g += Graph().parse('properties.rdf')
g += Graph().parse('resources.rdf')
g += Graph().parse('scripts.rdf' )
#g += Graph().parse('services.nt', format='nt')
#g += Graph().parse('technologies.nt', format='nt')

open('complete.nt', 'w').write(g.serialize(format='nt'))
open('complete.rdf', 'w').write(g.serialize())


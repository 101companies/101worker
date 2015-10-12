#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Martin Leinberger'

import os
import json
import urllib

import rdflib
from rdflib import URIRef

import sesame

from helpers.ValidationModels import ConceptModel, Property, WikiResource, WikiConcept
from helpers.Errorlog import serializeLog

# Setting up namespaces
#ontology = rdflib.Namespace('http://101companies.org/ontology#')
#resources = rdflib.Namespace('http://101companies.org/resources#')
#rdf = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
#rdfs = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')


def encode(s):
    return urllib.quote(s.replace(unichr(252), 'ue').replace(unichr(228), 'ae').replace(unichr(246), 'oe')
                        .replace(unichr(232), 'e').replace(unichr(233), 'e').replace(unichr(234), 'e')
                        .replace(unichr(244), 'o').replace(unichr(249), 'u').replace(unichr(251), 'u')
                        .replace(unichr(252), 'o').replace(unichr(225), 'a').replace(unichr(237), 'i')
                        .replace(unichr(241), 'n').replace(unichr(243), 'o').replace(unichr(250), 'u')
                        .replace(unichr(252), 'u').replace(' ', '_'))

def isResource(description): return (not 'isA' in description) and (not description['p'] == 'Namespace')

# Issue aus der Liste machen um die Liste von Namespaces zu diskutieren
def shouldBeSkipped(description): return description.get('p', '') in ['Dotnet', 'Information', 'Module',
                                                                      '101companies', 'Namespace', 'Issue', 'Java',
                                                                      'Property', '101', 'Category' ]


def main():
    # Building the model defined in the json based language
    for modelFile in filter(lambda x: x.endswith('.json'), os.listdir('./../validate/models')):
        ConceptModel(json.load(open(os.path.join('./../validate/models', modelFile))))

    # Creating the graph
    graph = rdflib.Graph()
    graph.bind('onto', URIRef('http://101companies.org/ontology#'))
    graph.bind('res', URIRef('http://101companies.org/resources#'))

    # Adding triples representing the models to the graph
    for clss in ConceptModel.Models.values():
        for t in clss.toRDF():
            graph.add(t)

    for property in Property.Properties.values():
        for t in property.toRDF():
            graph.add(t)


    for page in json.load(open('./../../../101web/data/dumps/wiki.json', 'r'))['wiki']['pages']:
        if not shouldBeSkipped(page):
            if isResource(page):
                triples = WikiResource(page).toRDF()
            else:
                triples = WikiConcept(page).toRDF()

            for t in triples:
                graph.add(t)


    serialized_version = 'graph.rdf'
    open(serialized_version, 'w').write(graph.serialize())
    serializeLog('errors.json')

    uri = 'http://triples.101companies.org:8080/openrdf-sesame/repositories/sandbox'
    response, content = sesame.clear_graph(uri)
    assert response['status'] == '204'
    response, content = sesame.upload(uri, serialized_version)


if __name__ == '__main__':
    print 'Starting process'
    main()
    print 'Finished... '

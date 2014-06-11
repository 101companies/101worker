#! /usr/bin/env python

__author__ = 'Martin Leinberger'

import os
import sys
import json
import rdflib
from rdflib import URIRef
from rdfalchemy.sparql.sesame2 import SesameGraph
import urllib
import httplib2

sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')

from metamodel import Dumps

# Setting up namespaces
ontology = rdflib.Namespace('http://101companies.org/ontology#')
resources = rdflib.Namespace('http://101companies.org/resources#')
rdf = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rdfs = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')



# Keys to be ignored for general mapping - they might however be processed in a more specific part of the code
ignored_keys_in_contributions = ['p', 'n', 'instanceOf', 'internal_links', 'headline', 'identifies', 'subresources']
ignored_keys_in_subresources = ['internal_links']
ignored_keys_general = ['p', 'n', 'instanceOf', 'headline', 'internal_links', 'linksTo', 'isA', 'identifies', 'subresources']


def clear_sesame_graph(uri):
    endpoint = os.path.join(uri, 'statements')
    data = "update=CLEAR ALL"
    (response, content) = httplib2.Http().request(endpoint, 'POST', body=data,
                                                  headers={ 'content-type': 'application/x-www-form-urlencoded',
                                                            'accept': 'application/sparql-update'})
    print response
    assert response['status'] == '204'

def collect(wiki):
    collection = []
    namespace_of_interest = json.load(open('interesting_namespaces.json', 'r'))
    blacklist = json.load(open('pages.json', 'r'))
    #interesting_pages = json.load(open('pages.json', 'r'))
    for page in wiki:
        if page['p'] in namespace_of_interest and not (page['p'] + ":" + page['n'].replace(' ', '_')) in blacklist:
        # name = page['p'] + ":" + page['n'].replace(' ', '_')
        # if name in interesting_pages:
            collection.append(page)
    return collection


def encode(s):
    return urllib.quote(s)


def encodeOntology(s):
    return ontology[ encode(s) ]


def encodeResource(s):
    return resources[ encode(s) ]


def make_ontology_classes(graph):
    # Add highest level classes
    wikipage = encodeOntology('WikiPage')
    graph.add( (wikipage, rdf['type'], rdfs['Class']) )
    # TODO What's the point of this
    one_oh_one_thing = encodeOntology('OneOhOneThing')
    graph.add( (one_oh_one_thing, rdf['type'], rdfs['Class']) )

    for ns in ['Contribution', 'Technology', 'Language', 'Concept', 'Feature']:
        thing = encodeOntology(ns)
        page = encodeOntology(ns+'Page')

        graph.add( (thing, rdf['type'], rdfs['Class']) )
        graph.add( (thing, rdfs['subClassOf'], one_oh_one_thing))

        graph.add( (page, rdf['type'], rdfs['Class']) )
        graph.add( (page, rdfs['subClassOf'], wikipage))

def make_contribution_resource(page, graph):
    # Make unique name for this contribution
    uri = encodeResource(page['n'])

    # Add types to URI (Contributions are instances of the Contribution class and of the contribution page)
    # TODO: Are there any other classes that need to be considered?
    graph.add( (uri, rdf['type'], encodeOntology('Contribution')) )
    graph.add( (uri, rdf['type'], encodeOntology('ContributionPage')) )

    # Add remaining predicates
    for key in filter(lambda x: x not in ignored_keys_in_contributions, page):
        predicate = encodeOntology(key)
        for p in page[key]:
            target_uri = encodeResource(p['n'])
            graph.add((uri, predicate, target_uri))


def make_general_resource(page, graph):
    # Make unique name for this resource
    if 'isA' in page:
        uri = encodeOntology( page['n'] )
    else:
        uri = encodeResource( page['n'] )


    # Add types
    graph.add( (uri, rdf['type'], encodeOntology(page['p'] + 'Page')) )
    for type in page.get('instanceOf', []):
        target_uri = type['n']
        graph.add( (uri, rdf['type'], encodeOntology(target_uri)) )

    # Add subclass relationships
    for isA in page.get('isA', []):
        target_uri = isA['n']
        graph.add( (uri, rdfs['subClassOf'], encodeOntology(target_uri)) )

    # Deal with subresources
    for sub_resource_name in page.get('subresources',{}):
        sub_resource_uri = uri + '#' + encode(sub_resource_name)
        sub_resource = page['subresources'][sub_resource_name]
        for key in filter(lambda x: x not in ignored_keys_in_subresources, sub_resource):
            predicate = encodeOntology(key)
            for p in sub_resource[key]:
                target_uri = p['n']
                graph.add( (sub_resource_uri, predicate, encodeResource(target_uri)) )

    # Convert linksTo
    for link in page.get('linksTo', []):
        graph.add( (uri, encodeOntology('linksTo'), URIRef(urllib.quote(link))) )

    # Add remaining predicates
    for key in filter(lambda x: x not in ignored_keys_general, page):
        predicate = encodeOntology(key)
        for p in page[key]:
            target_uri = p['n']
            graph.add((uri, predicate, encodeResource(target_uri)))


def main():
    uri = 'http://triples.101companies.org/openrdf-sesame/repositories/ML_testing'

    clear_sesame_graph(uri)

    graph = SesameGraph(uri)
    wiki = Dumps.WikiDump()

    mapping_rules = {
        # Special cases
        'Contribution': make_contribution_resource,

        # General cases
        'Technology': make_general_resource,
        'Language': make_general_resource,
        'Concept': make_general_resource,
        'Feature': make_general_resource
    }

    # Starting to add stuff
    print 'Adding ontology classes'
    make_ontology_classes(graph)

    print 'Adding data from wiki pages'
    for page in collect(wiki):
        print "dealing with page {}".format(page)
        mapping_func = mapping_rules[page['p']]
        mapping_func(page, graph)

    #print graph.serialize(format='n3')


if __name__ == '__main__':
    print 'Starting process'
    main()
    print 'Finished'
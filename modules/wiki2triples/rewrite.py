#! /usr/bin/env python
# -*- coding: utf-8 -*-
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
ignored_keys_in_contributions = ['p', 'n', 'instanceOf', 'internal_links', 'headline', 'identifies', 'subresources',
                                 'similarTo', 'linksTo', 'sameAs', 'relatesTo']
ignored_keys_in_subresources = ['internal_links']
ignored_keys_general = ['p', 'n', 'instanceOf', 'headline', 'internal_links', 'linksTo', 'isA', 'identifies',
                        'subresources', 'similarTo', 'sameAs', 'relatesTo']
ignored_keys_for_validation  = ['p', 'n', 'headline', 'internal_links', 'subresources', 'isA']

# Hacking in the allowed relations real quick:
models = ["concept", "contribution", "contributor", "feature", "language",
          "technology", "vocabulary"]
allowed_relations = {}
erroneous_pages = []

for model in models:
    allowed_relations[model] = []
    x = json.load(urllib.urlopen("http://worker.101companies.org/data/onto/models/"+model+".json"))
    for property in x.get('properties', []):
        allowed_relations[model].append(property['property'])

    # Other models inherit from the concept model
    for y in filter(lambda x: x not in ['concept'], allowed_relations.keys()):
        allowed_relations[y] += (allowed_relations['concept'])


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
    namespace_blacklist = json.load(open('namespaces_blacklist.json', 'r'))
    #blacklist = json.load(open('pages.json', 'r'))
    #interesting_pages = json.load(open('pages.json', 'r'))
    for page in wiki:
        #collection.append(page)
        if not page['p'] in namespace_blacklist and page['p'].lower() in allowed_relations: #and not (page['p'] + ":" + page['n'].replace(' ', '_')) in blacklist:
        # name = page['p'] + ":" + page['n'].replace(' ', '_')
        # if name in interesting_pages:
            collection.append(page)
    return collection


def encode(s):
    return urllib.quote(s.replace(unichr(252), 'ue').replace(unichr(228), 'ae').replace(unichr(246), 'oe')
                        .replace(unichr(232), 'e').replace(unichr(233), 'e').replace(unichr(234), 'e')
                        .replace(unichr(244), 'o').replace(unichr(249), 'u').replace(unichr(251), 'u')
                        .replace(unichr(252), 'o').replace(unichr(225), 'a').replace(unichr(237), 'i')
                        .replace(unichr(241), 'n').replace(unichr(243), 'o').replace(unichr(250), 'u')
                        .replace(unichr(252), 'u').replace(' ', '_'))


def encodeOntology(s):
    return ontology[ encode(s) ]


def encodeResource(s):
    return resources[ encode(s) ]


def make_ontology_classes(graph):
    # Add highest level classes
    wikipage = encodeOntology('WikiPage')
    graph.add( (wikipage, rdf['type'], rdfs['Class']) )

    concept = encodeOntology('Concept')
    conceptPage = encodeOntology('ConceptPage')

    graph.add( (concept, rdf['type'], rdfs['Class']) )
    graph.add( (conceptPage, rdf['type'], rdfs['Class']) )
    graph.add( (conceptPage, rdfs['subClassOf'], wikipage))

    for ns in ['Contribution', 'Technology', 'Language', 'Feature']:
        thing = encodeOntology(ns)
        page = encodeOntology(ns+'Page')

        graph.add( (thing, rdf['type'], rdfs['Class']) )
        graph.add( (thing, rdfs['subClassOf'], concept))

        graph.add( (page, rdf['type'], rdfs['Class']) )
        graph.add( (page, rdfs['subClassOf'], wikipage))


def make_contribution_resource(page, graph):
    print page['n']

    # Make unique name for this contribution
    uri = encodeResource(page['n'])

    # Add types to URI (Contributions are instances of the Contribution class and of the contribution page)
    # TODO: Are there any other classes that need to be considered?
    graph.add( (uri, rdf['type'], encodeOntology('Contribution')) )
    graph.add( (uri, rdf['type'], encodeOntology('ContributionPage')) )

    # Convert linksTo
    for link in page.get('linksTo', []):
        graph.add( (uri, encodeOntology('linksTo'), URIRef(urllib.quote(link))) )

    for link in page.get('similarTo', []):
        graph.add( (uri, encodeOntology('similarTo'), URIRef(urllib.quote(link))) )

    for link in page.get('sameAs', []):
        graph.add( (uri, encodeOntology('sameAs'), URIRef(urllib.quote(link))) )

    # Add remaining predicates
    for key in filter(lambda x: x not in ignored_keys_in_contributions, page):
        predicate = encodeOntology(key)
        for p in page[key]:
            target_uri = encodeResource(p['n'])
            graph.add((uri, predicate, target_uri))

    # Sorry, I know this is ugly, but I don't ahve time to properly refactor this stuff
    # Loop over internal links for mentions statements
    for internal_link in page.get('internal_links', []):
        if not '::' in internal_link:
            if ':' in internal_link:
                p, n = internal_link.split(':')[0], internal_link.split(':')[1]
            else:
                n = internal_link
            graph.add( (uri, encodeOntology('mentions'), encodeResource(n)) )

    # Error check
    for key in filter(lambda x: x not in ignored_keys_for_validation, page):
        if not ('onto:'+key) in allowed_relations['contribution']:
            erroneous_pages.append({'page': (page['p']+':'+page['n']), 'invalid relation': key})


def make_general_resource(page, graph):
    print page['n']
    # Make unique name for this resource
    if 'isA' in page:
        uri = encodeOntology( page['n'] )
    else:
        uri = encodeResource( page['n'] )


    # Add types
    graph.add( (uri, rdf['type'], encodeOntology(page['p'] + 'Page')) )
    if not page['p'] == 'Concept':
        graph.add( (uri, rdf['type'], encodeOntology(page['p'])) )

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

    for link in page.get('similarTo', []):
        graph.add( (uri, encodeOntology('similarTo'), URIRef(urllib.quote(link))) )

    for link in page.get('sameAs', []):
        graph.add( (uri, encodeOntology('sameAs'), URIRef(urllib.quote(link))) )

    # Add remaining predicates
    for key in filter(lambda x: x not in ignored_keys_general, page):
        predicate = encodeOntology(key)
        for p in page[key]:
            target_uri = p['n']
            graph.add((uri, predicate, encodeResource(target_uri)))

    # Sorry, I know this is ugly, but I don't ahve time to properly refactor this stuff
    # Loop over internal links for mentions statements
    for internal_link in page.get('internal_links', []):
        if not '::' in internal_link:
            if ':' in internal_link:
                p, n = internal_link.split(':')[0], internal_link.split(':')[1]
            else:
                n = internal_link
            graph.add( (uri, encodeOntology('mentions'), encodeResource(n)) )

    # Error check
    for key in filter(lambda x: x not in ignored_keys_for_validation, page):
        if not ('onto:'+key) in allowed_relations[page['p'].lower()]:
            erroneous_pages.append({'page': (page['p']+':'+page['n']), 'invalid relation': key})


def main():
    #uri = 'http://triples.101companies.org/openrdf-sesame/repositories/ML_testing'
    uri = 'http://triples.101companies.org/openrdf-sesame/repositories/Testing_2'
    #clear_sesame_graph(uri)
    #graph = SesameGraph(uri)
    graph = rdflib.Graph()
    graph.bind('onto', 'http://101companies.org/ontology#')
    graph.bind('res', 'http://101companies.org/resources#')

    wiki = Dumps.WikiDump()

    mapping_rules = {
        # Special cases
        'Contribution': make_contribution_resource,

        # General cases
        'Technology': make_general_resource,
        'Language': make_general_resource,
        'Concept': make_general_resource,
        'Feature': make_general_resource,
        'Contributor': make_general_resource,
    }

    # Starting to add stuff
    print 'Adding ontology classes'
    make_ontology_classes(graph)

    print 'Adding data from wiki pages'
    for page in collect(wiki):
        #print "dealing with page {}".format(page)
        if page['p'] in mapping_rules:
            mapping_func = mapping_rules[page['p']]
            mapping_func(page, graph)
        else:
            make_general_resource(page, graph)

    print 'Writing graph.rdf...'
    open('graph.rdf', 'w').write(graph.serialize())

    print 'Clearing Sesame...'
    clear_sesame_graph(uri)

    print 'Uploading serialized file...'
    params     = { 'context': '<' + 'http://101companies.org' + '>' }
    endpoint = "http://141.26.71.114/openrdf-sesame/repositories/Testing_2/statements?%s" % (urllib.urlencode(params))
    data = open('graph.rdf', 'r').read()
    (response, content) = httplib2.Http().request(endpoint, 'PUT', body=data, headers={ 'content-type': 'application/rdf+xml' })
    print 'Response was {}'.format(response)
    print content

    #graph.serialize(destination='./graph.n3', format='n3')
    #print graph.serialize(format='n3')

if __name__ == '__main__':
    print 'Starting process'
    main()
    print 'Finished... '
    json.dump(erroneous_pages, open('./erroneous_pages.json', 'w'))
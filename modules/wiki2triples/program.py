#! /usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Martin Leinberger'

import os
import sys
import json
import rdflib
from rdflib import URIRef
import urllib
import sesame
sys.path.append('../../libraries')
sys.path.append('../../libraries/101meta')

from metamodel import Dumps

# Setting up namespaces
ontology = rdflib.Namespace('http://101companies.org/ontology#')
resources = rdflib.Namespace('http://101companies.org/resources#')
rdf = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rdfs = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')

namespace_cache = {}
classes_in_wiki = []
debug = {}
premodeled_classes = []

def get_namespace(namespace_name):
    if not namespace_name in namespace_cache:
        namespace_cache[namespace_name] = rdflib.Namespace('http://101companies.org/resources/'+namespace_name.strip()+'#')
    return namespace_cache[namespace_name]


# Keys to be ignored for general mapping - they might however be processed in a more specific part of the code
allowed_relations = {}
erroneous_pages = []


ignored_keys_validation = ['p', 'n', 'headline', 'internal_links', 'subresources', 'isA']
ignored_keys_in_instances = ['p', 'n', 'instanceOf', 'isA', 'headline', 'internal_links', 'subresources']
ignored_keys_in_classes = ignored_keys_in_instances
ignored_keys_in_subresources = ['internal_links']


# revise, as this is just plain awful
models = filter(lambda x: '.json' in x, os.listdir('./../validate/models'))
for model in models:
    model_name = model.replace('.json', '')
    allowed_relations[model_name] = []
    x = json.load(open('../validate/models/' + model, 'r'))
    for property in x.get('properties', []):
        allowed_relations[model_name].append(property['property'])
#print allowed_relations
for y in filter(lambda x: x not in ['entity'], allowed_relations.keys()):
    allowed_relations[y] += allowed_relations['entity']

overloading_table = {}
def build_overloading_table():
    for m in filter(lambda x: '.json' in x, os.listdir('./../onto2ttl/models')):
        data = json.load(open('./../onto2ttl/models/' + m, 'r'))
        property_domain = data['@id']
        for property in data.get('properties',[]):
            if property.get('super', None):
                super_property = property['super']
                property_range = property['range']
                overloading_table.setdefault(super_property, {})[(property_domain, property_range)] =\
                    property['property']


def page_mapping(ns, s):
    if not ns: ns = 'Concept'
    map = {
            'software language' : 'Language',
            'software technology': 'Technology',
            'software concept' : 'Concept',
            'software feature' : 'Feature'
        }
    if s.lower() in map and ns == 'Concept':
        print 'Mapping {} to {}'.format(s, map[s.lower()])
        s = map[s.lower()]
        return s

    return s


def filter_pages(wiki):
    collection = []
    namespace_blacklist = json.load(open('namespaces_blacklist.json', 'r'))
    for page in wiki:
        if not page['p'] in namespace_blacklist and page['p'].lower() in allowed_relations: #and not (page['p'] + ":" + page['n'].replace(' ', '_')) in blacklist:
            collection.append(page)
    return collection


def encode(s):
    return urllib.quote(s.replace(unichr(252), 'ue').replace(unichr(228), 'ae').replace(unichr(246), 'oe')
                        .replace(unichr(232), 'e').replace(unichr(233), 'e').replace(unichr(234), 'e')
                        .replace(unichr(244), 'o').replace(unichr(249), 'u').replace(unichr(251), 'u')
                        .replace(unichr(252), 'o').replace(unichr(225), 'a').replace(unichr(237), 'i')
                        .replace(unichr(241), 'n').replace(unichr(243), 'o').replace(unichr(250), 'u')
                        .replace(unichr(252), 'u').replace(' ', '_'))


def encode_predicate(p):
    return encode_ontology('onto',p[0].lower() + p[1:])


def encode_ontology(namespace, s):
    s = page_mapping(namespace, s)
    return ontology[ encode(s) ]


def encode_resource(namespace, s):
    if not namespace: namespace = 'Concept'
    s = page_mapping(namespace, s)
    return get_namespace(namespace)[ encode(s) ]


def make_wiki_link(p):
    wiki_uri = 'http://www.101companies.org/wiki/'
    if p['p'] and not p['p'] == 'Concept':
        return wiki_uri + p['p'] + ':' + p['n']
    else:
        return wiki_uri + p['n']


def disambiguate(p):
    if 'http://' in p:
        try:
            return None, rdflib.Literal(p)
        except:
            debug.setdefault('non_convertable_uris', []).append(p)
            return None, URIRef('http://failedConversion.com')

    if ':' in p:
        namespace, name = p.split(':')[0], p.split(':')[1]
    else:
        if isinstance(p, basestring):
            namespace, name = 'Concept', p
        else:
            namespace, name = p['p'], p['n']
            if not namespace: namespace = 'Concept'
    if name in classes_in_wiki or (namespace+':'+name) in classes_in_wiki:
        return 'Concept', encode_resource('Concept', name)
    else:
        return namespace, encode_resource(namespace, name)


# def hardcoded_classes(graph):
#     # Adding most basic classes
#     entity = encode_ontology('onto', 'Entity')
#     wikipage = encode_ontology('onto', 'WikiPage')
#     classifier = encode_ontology('onto', 'Classifier')
#
#     for s in [entity, wikipage, classifier]:
#         triple = (s, rdf['type'], rdfs['Class'])
#         graph.add(triple)
#
#     # Adding instruments
#     instrument = encode_ontology('onto', 'Instrument')
#     graph.add((instrument, rdf['type'], rdfs['Class']))
#     graph.add((instrument, rdfs['subClassOf'], entity))
#
#     for s in [encode_ontology('onto', 'Language'), encode_ontology('onto', 'Technology'), encode_ontology('onto', 'Concept')]:
#         triple = s, rdfs['subClassOf'], instrument
#         graph.add(triple)
#
#         #TODO Check again with Ralf and Andrei
#         triple = s, rdfs['subClassOf'], wikipage
#         graph.add(triple)
#
#     # Add remaining classes
#     for s in ['Contribution', 'Contributor', 'Feature', 'Script', 'Course']:
#         s = encode_ontology('onto', s)
#         triple = (s, rdfs['subClassOf'], entity)
#         graph.add(triple)


def map_instance(page, graph):
    def class_for_page():
        if page['p']: return page['p']
        else: return 'Concept'

    clss = class_for_page()
    domain_for_relation = clss
    uri = encode_resource(clss, page['n'])

    triple = uri, rdf['type'], encode_ontology('onto', 'WikiPage')
    graph.add(triple)

    triple = uri, rdf['type'], encode_ontology('onto', clss)
    graph.add(triple)

    triple = uri, encode_predicate('hasHeadline'), rdflib.Literal(page['headline'])
    graph.add(triple)

    triple = uri, encode_predicate('hasWikiLink'), rdflib.Literal(make_wiki_link(page))
    graph.add(triple)

    for o in page.get('instanceOf', []):
        triple = uri, rdf['type'], encode_ontology(o['p'], o['n'])
        graph.add(triple)
        triple = encode_ontology(o['p'], o['n']), rdf['type'], encode_ontology('onto', 'Classifier')
        if not o['p'] and not page_mapping(o['p'], o['n']) in premodeled_classes:
            print 'Adding additional rdf:type onto:Classifier statement for {}'.format(o['n'])
            graph.add(triple)

    #TODO handle sub resources
    for sub_resource_name in page.get('subresources',{}):
        sub_resource_uri = uri + '#' + encode(sub_resource_name)
        sub_resource = page['subresources'][sub_resource_name]
        for key in filter(lambda x: x not in ignored_keys_in_subresources, sub_resource):
            predicate = encode_predicate(key)
            for p in sub_resource[key]:
                target_clss, target = disambiguate(p)
                predicate = overloading_table.get(predicate, {}).get((clss, target_clss), predicate)
                graph.add( (sub_resource_uri, predicate, target) )

    #Remaining predicates should all be in internal links
    for link in page.get('internal_links', []):
        # Determine predicate
        if '::' in link:
            predicate = link.split('::')[0]
            target_clss, obj = disambiguate(link.split('::')[1])
        else:
            predicate = 'mentions'
            target_clss, obj = disambiguate(link)

        if (predicate[0].lower() + predicate[1:]) not in ignored_keys_in_instances:
            #print predicate
            #if predicate.lower() == 'uses':  
                #print "{}, {}".format(clss, target_clss)
                #print json.dumps(overloading_table, indent=4)
                #raise Exception("my stop")
            predicate = overloading_table.get(predicate.lower(), {}).get((clss, target_clss), predicate)
            triple = uri, encode_predicate(predicate), obj
            graph.add(triple)
            


def map_class(page, graph):
    # I dislike this - I should really make this call map_instance for the instance part
    onto_entity = encode_ontology(page['p'], page['n'])

    triple = onto_entity, rdf['type'], rdfs['Class']
    graph.add(triple)

    if not page_mapping(page['p'], page['n']) in premodeled_classes:
        triple = onto_entity, rdf['type'], encode_ontology('onto', 'Classifier')
        graph.add(triple)

    triple = onto_entity, rdfs['comment'], rdflib.Literal(page['headline'])
    graph.add(triple)

    for o in page.get('isA', []):
        triple = onto_entity, rdfs['subClassOf'], encode_ontology(o['p'], o['n'])
        graph.add(triple)

    triple = onto_entity, encode_predicate('classifies'), get_namespace('Concept')[encode(page['n'])]
    graph.add(triple)

    # Normal instance part
    clss = 'Concept'
    uri = encode_resource(clss, page['n'])

    triple = uri, rdf['type'], encode_ontology('onto', clss)
    graph.add(triple)

    triple = uri, rdf['type'], encode_ontology('onto', 'WikiPage')
    graph.add(triple)

    triple = uri, encode_predicate('hasHeadline'), rdflib.Literal(page['headline'])
    graph.add(triple)

    triple = uri, encode_predicate('hasWikiLink'), rdflib.Literal(make_wiki_link(page))
    graph.add(triple)

    #TODO handle sub resources
    for sub_resource_name in page.get('subresources',{}):
        sub_resource_uri = uri + '#' + encode(sub_resource_name)
        sub_resource = page['subresources'][sub_resource_name]
        for key in filter(lambda x: x not in ignored_keys_in_subresources, sub_resource):
            predicate = encode_predicate(key)
            for p in sub_resource[key]:
                target_clss, target = disambiguate(p)
                predicate = overloading_table.get(predicate, {}).get((clss, target_clss), predicate)
                graph.add( (sub_resource_uri, predicate, target) )

    #Remaining predicates should all be in internal links
    for link in page.get('internal_links', []):
        # Determine predicate
        if '::' in link:
            predicate = link.split('::')[0]
            target_clss, obj = disambiguate(link.split('::')[1])
        else:
            predicate = 'mentions'
            target_clss, obj = disambiguate(link)

        if (predicate[0].lower() + predicate[1:]) not in ignored_keys_in_classes:
            predicate = overloading_table.get(predicate, {}).get((clss, target_clss), predicate)
            triple = uri, encode_predicate(predicate), obj
            graph.add(triple)

    for key in filter(lambda x: x not in ignored_keys_validation, page):
        if not ('onto:'+key) in allowed_relations[page['p'].lower()]:
            erroneous_pages.append({'page': (page['p']+':'+page['n']), 'invalid relation': key})


def map_page(page, graph):
    print 'Converting {}:{}'.format(page['p'],page['n'])
    is_instance = not 'isA' in page

    if is_instance:
        map_instance(page, graph)
    else:
        map_class(page, graph)


def main():
    uri = 'http://141.26.71.163:8080/openrdf-sesame/repositories/sandbox'
    serialized_version = 'graph.rdf'

    print 'Building overloading table'
    build_overloading_table()

    print 'Initializing graph'
    graph = rdflib.Graph()
    graph.bind('onto', 'http://101companies.org/ontology#')
    graph.bind('res', 'http://101companies.org/resources#')

    print 'Filtering wiki pages'
    wiki = filter_pages(Dumps.WikiDump())

    print 'Adding hardcoded (ontology) classes'
    path_to_ontology = '../../../101web/data/onto/ttl'
    for ont_def in filter(lambda x: '.ttl' in x, os.listdir(path_to_ontology)):
        premodeled_classes.append(ont_def[0].upper() + ont_def[1:])
        print 'Parsing ' + ont_def
        graph.parse(os.path.join(path_to_ontology, ont_def), format='turtle')
    #graph.parse('additional_triples.ttl', format='turtle')
    graph.add((encode_ontology('onto', 'WikiPage'), rdf['type'], rdfs['Class']))

    #hardcoded_classes(graph)
    #print 'Adding ontology classes'
    #make_ontology_classes(graph)

    # Building up cache to determine whether the relation is to a class or a instance
    # Do I really need this?
    for page in wiki:
        if 'isA' in page:
            if not page.get('p', None): link = page['p'] + ':' + page['n']
            else: link = 'Concept:' + page['n']
            classes_in_wiki.append(link)

    print 'Starting conversion'
    for page in wiki:
        map_page(page, graph)

    print 'Adding namespaces to graph'
    for key in namespace_cache.keys():
        graph.bind(key, namespace_cache[key])

    print 'Serializing graph...'
    open(serialized_version, 'w').write(graph.serialize())
    
    #print overloading_table
    print 'Clearing Sesame...'
    response, content = sesame.clear_graph(uri)
    assert response['status'] == '204'

    print 'Uploading serialized file...'
    response, content = sesame.upload(uri, serialized_version)


if __name__ == '__main__':
    print 'Starting process'
    main()
    print 'Finished... '
    json.dump(erroneous_pages, open('./erroneous_pages.json', 'w'))

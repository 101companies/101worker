#! /usr/bin/env python

import rdflib
import json

problems = []
alreadyVisited = []
blacklist = json.load(open('blacklist.json', 'r'))
typeRef = rdflib.URIRef('http://www.w3.org/1999/02/22-rdf-syntax-ns#type')
childrenMap = {
    rdflib.URIRef('http://101companies.org/property/Namespace'): [
        rdflib.URIRef('http://101companies.org/property/member')
    ],
    rdflib.URIRef('http://101companies.org/property/Member'): [
        rdflib.URIRef('http://101companies.org/property/folder'),
        rdflib.URIRef('http://101companies.org/property/file')
    ],
    rdflib.URIRef('http://101companies.org/property/Folder'): [
        rdflib.URIRef('http://101companies.org/property/folder'),
        rdflib.URIRef('http://101companies.org/property/file')
    ],
    rdflib.URIRef('http://101companies.org/property/File'): [
        rdflib.URIRef('http://101companies.org/property/fragment')
    ],
    rdflib.URIRef('http://101companies.org/property/Fragment'): [
        rdflib.URIRef('http://101companies.org/property/fragment')
    ]
}


def load(url):
    g2 = rdflib.Graph()
    g2.load(url)
    return g2

def extract(url, followLinks = True):
    if str(url) in alreadyVisited:
        raise Exception(url + ' gets visited twice (Circle)')
    alreadyVisited.append(str(url))
    print 'extracting {}'.format(url)
    g = load(url)

    if followLinks:
        childPredicate = None
        for subject, predicate, object in g.triples((None, typeRef, None)):
            childPredicate = object
        if childPredicate:
            for p in childrenMap.get(childPredicate, []):
                for s, pr, o in g.triples((None, p, None)):
                    if not any(substring in str(o) for substring in blacklist):
                        try:
                            g += extract(o)
                        except Exception as e:
                            problems.append({
                                'reason': str(e),
                                'onObject': str(o)
                            })
                            print 'extracting {} failed'.format(object)

    return g

oneOhOne = extract('http://101companies.org/resources/101?format=rdf')
open('oneOhOne.rdf', 'w').write(oneOhOne.serialize())

course = extract('http://101companies.org/resources/courses?format=rdf')
open('course.rdf', 'w').write(course.serialize())

features = extract('http://101companies.org/resources/features?format=rdf')
open('features.rdf', 'w').write(features.serialize())

information = extract('http://101companies.org/resources/information?format=rdf')
open('information.rdf', 'w').write(information.serialize())

properties = extract('http://101companies.org/resources/properties?format=rdf')
open('properties.rdf', 'w').write(properties.serialize())

resources = extract('http://101companies.org/resources/resources?format=rdf')
open('resources.rdf', 'w').write(resources.serialize())

scripts = extract('http://101companies.org/resources/scripts?format=rdf')
open('scripts.rdf', 'w').write(scripts.serialize())

services = extract('http://101companies.org/resources/services?format=rdf')
open('services.rdf', 'w').write(services.serialize())

concepts = extract('http://101companies.org/resources/concepts?format=rdf')
open('concepts.nt', 'w').write(concepts.serialize())

languages = extract('http://101companies.org/resources/languages?format=rdf')
open('languages.rdf', 'w').write(languages.serialize())

technologies = extract('http://101companies.org/resources/technologies?format=rdf')
open('technologies.rdf', 'w').write(technologies.serialize())

contributions = extract('http://101companies.org/resources/contributions?format=rdf')
open('contributions.rdf', 'w').write(contributions.serialize())

#themes = extract('http://101companies.org/resources/themes?format=rdf')
#open('themes.nt', 'w').write(themes.serialize(format='nt'))

#vocabulary = extract('http://101companies.org/resources/vocabularies?format=rdf')
#open('vocabulary.nt', 'w').write(vocabulary.serialize(format='nt'))

#modules = extract('http://101companies.org/resources/modules?format=rdf')
#open('modules.nt', 'w').write(modules.serialize(format='nt'))


json.dump(problems, open('problems.json', 'w'), indent=4)
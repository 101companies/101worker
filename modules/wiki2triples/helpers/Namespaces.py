#! /usr/bin/env python

import rdflib

__author__ = 'Martin Leinberger'

ontology = rdflib.Namespace('http://101companies.org/ontology#')
resources = rdflib.Namespace('http://101companies.org/resources#')
rdf = rdflib.Namespace('http://www.w3.org/1999/02/22-rdf-syntax-ns#')
rdfs = rdflib.Namespace('http://www.w3.org/2000/01/rdf-schema#')

namespacesByName = {
    'Technology'    : rdflib.Namespace('http://101companies.org/resources/Technology#'),
    'Language'      : rdflib.Namespace('http://101companies.org/resources/Language#'),
    'Concept'       : rdflib.Namespace('http://101companies.org/resources/Concept#'),
    'Document'      : rdflib.Namespace('http://101companies.org/resources/Document#'),
    'Feature'       : rdflib.Namespace('http://101companies.org/resources/Feature#'),
    'Contribution'  : rdflib.Namespace('http://101companies.org/resources/Contribution#'),
    'Theme'         : rdflib.Namespace('http://101companies.org/resources/Theme#'),
    'Contributor'   : rdflib.Namespace('http://101companies.org/resources/Contributor#'),
    'Course'        : rdflib.Namespace('http://101companies.org/resources/Course#'),
    'Script'        : rdflib.Namespace('http://101companies.org/resources/Script#'),
    'Tag'           : rdflib.Namespace('http://101companies.org/resources/Tag#'),
    'Vocabulary'    : rdflib.Namespace('http://101companies.org/resources/Vocabulary#'),
    'Service'       : rdflib.Namespace('http://101companies.org/resources/Service#'),
    'Term'          : rdflib.Namespace('http://101companies.org/resources/Term#'),
    '101companies'  : rdflib.Namespace('http://101companies.org/resources#'), # should this one really be in there
    '101term'       : rdflib.Namespace('http://101companies.org/resources/101term#'),
    'Information'   : rdflib.Namespace('http://101companies.org/resources#Information'),
    'Architecture'  : rdflib.Namespace('http://101companies.org/resources/Architecture#'),
    'Property'      : rdflib.Namespace('http://101companies.org/resources/Property#'),
    'Relatesto'     : rdflib.Namespace('http://101companies.org/resources/RelatesTo#'),
    'Rdf'           : rdf,
    'Rdfs'          : rdfs,
    'Ontology'      : ontology,
    'Namespace'     : ontology
}

def nameSpaceByName(ns):
    ns = ns.strip()
    ns = ns[:1].upper() + ns[1:].lower()
    return namespacesByName[ns]

#!/usr/bin/env python3
# coding=utf-8

try:
    from pymongo import MongoClient
    from bson.json_util import dumps
except ImportError:
    print('Error: pymongo is missing: "pip3 install pymongo"')

try:
    from rdflib import ConjunctiveGraph, Graph, URIRef, BNode, Literal, RDF, Namespace
    from rdflib.store import NO_STORE, VALID_STORE
    from rdflib.namespace import FOAF, DC
    import rdflib.graph as g
    import urllib.parse
    from bson.son import SON
    import glob
except ImportError:
    print('Error: rdflib is missing: "pip3 install rdflib"')

import json
import os
import glob

show_prints = True
debug = True
#debug = False
pageurl = "http://101companies.org/"
if debug:
    pageurl = "http://localhost:3000/"

ref_wikipage = URIRef(pageurl + "ld/ressources/101wikipage")
ref_repo = URIRef(pageurl + "ld/ressources/101repo")
ref_lable = URIRef("http://www.w3.org/2000/01/rdf-schema#label")
ref_created = URIRef("http://purl.org/dc/terms/created")

def import_repo(context, graph):
    msg ("import repo into graph")

    msg ("done")

def import_workermodules(context, graph):
    msg ("import worker and modules into graph")

    msg ("done")

def import_resources_and_dumps(context, graph):
    msg ("import resources and dumps into graph")

    msg ("done")

def import_wikipages(context, graph):
    msg ("import wikipages into graph")

    msg ("done")

def import_conceptual_data(context, graph):
    msg ("import conceptual data into graph")

    msg ("done")

def msg(txt):
    if(show_prints):
        print ("  " + txt)
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

except ImportError:
    print('Error: rdflib is missing: "pip3 install rdflib"')

import json
import os
import glob
import worker_lib

show_prints = True
debug = True
#debug = False
pageurl = "http://101companies.org/"
if debug:
    pageurl = "http://localhost:3000/"

def get_onto_uriref(name):
    return URIRef(pageurl + "resources/" + urllib.parse.quote(name))

ref_wikipage = URIRef(pageurl + "ld/ressources/101wikipage")
ref_repo = URIRef(pageurl + "ld/ressources/101repo")
ref_lable = URIRef("http://www.w3.org/2000/01/rdf-schema#label")
ref_created = URIRef("http://purl.org/dc/terms/created")

def import_repo(context, graph):
    msg ("import repo into graph")

    msg ("done")

def import_workermodules(context, graph):
    msg ("import worker and modules into graph")
    '''
    module_counter = 0
    for root, dirs, files in os.walk(context.get_env("modules101dir")):
        for file in files:
            if file.endswith("__init__.py"):
                txt = open(os.path.join(root, file))
                #print (txt.read().config)
                module_counter = module_counter + 1
                # print(os.path.join(root, file))
                # add_file(os.path.join(root, file), context, graph)
    graph = worker_lib.resolve_modules_graph(worker_lib.modules)
    msg (str(module_counter) + " modules found")

    #msg ("Or is it " + graph.count)
    '''
    msg ("done")

def import_resources_and_dumps(context, graph):
    msg ("import resources and dumps into graph")

    msg ("done")

def import_wikipages(context, graph):
    msg ("import wikipages into graph")
    wiki_links_json = context.read_dump('wiki-links')


    pages = wiki_links_json['wiki']['pages']
    types = ['Contribution',
             'Contributor',
             'Technology',
             'Language',
             'Features']

    sammler = []
    counter = 0
    for t in types:
        filtered  = filter(lambda p: t == p.get('p', ''), pages)
        for f in filtered:
            msg(t + ": " + f['n'])
            counter = counter +1

            scan(context, graph, 'Uses', f)
            #scan(context, graph, 'mentions', f)
            scan(context, graph, 'InstanceOf', f)
            scan(context, graph, 'MemberOf', f)


    msg("______ count: " + str(counter))

    for s in sammler:
        msg("typen: " + s)
def scan(context, graph, t, item):
    if (t in item):
        for u in item[t]:
            msg("  " + t + " " + u['n'])
            if ('p' in u and str(u['p']) != 'None'):
                if(item['n'] == 'jqueryDom'):
                    msg(str(u['p']))
                msg("    " + u['n'] + " is a " + u['p'])
                graph.add((get_onto_uriref(u['n']), RDF.type, get_onto_uriref(u['p'])))


def import_conceptual_data(context, graph):
    msg ("import conceptual data into graph")

    msg ("done")

def msg(txt):
    if(show_prints):
        print ("  " + txt)
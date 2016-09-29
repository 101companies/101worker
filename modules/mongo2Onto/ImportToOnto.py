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

class ImportToOnto(object):

    def __init__(self, _worker_context, _graph):
        self.debugmode = True
        # self.debugmode = False
        self.context = _worker_context
        self.graph = _graph
        self.pageurl = "http://101companies.org/"
        if self.debugmode:
            self.pageurl = "http://localhost:3000/"

        # set references:
        self.ref_wikipage = URIRef(self.pageurl + "ld/ressources/101wikipage")
        self.ref_repo = URIRef(self.pageurl + "ld/ressources/101repo")
        self.ref_lable = URIRef("http://www.w3.org/2000/01/rdf-schema#label")
        self.ref_created = URIRef("http://purl.org/dc/terms/created")

    def get_onto_uriref(self, name):
        return URIRef(self.pageurl + "resources/" + urllib.parse.quote(name.strip().lower()))

    def import_repo(self):
        '''
            imports the 101repo
            :param context: 101worker context object
            :param graph: Graph to be edited
            :return: nothing
            '''
        self.msg ("import repo into graph")

        self.msg ("done")

    def import_workermodules(self):
        '''
        imports the informations of 101worker and its modules based on ...
        :param context: 101worker context object
        :param graph: Graph to be edited
        :return: nothing
        '''
        self.msg ("import worker and modules into graph")
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
        self.msg ("done")

    def import_resources_and_dumps(self):
        '''
        imports informations about resources, dumps and their relations
        :param context: 101worker context object
        :param graph: Graph to be edited
        :return: nothing
        '''
        self.msg ("import resources and dumps into graph")

        self.msg ("done")

    def import_wikipages(self):
        '''
        imports the informations given by the wiki-pages based on the wiki-links.json dump
        :param context: 101worker context object
        :param graph: Graph to be edited
        :return: nothing
        '''
        self.msg ("import wikipages into graph")
        wiki_links_json = self.context.read_dump('wiki-links')

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
                self.msg(t + ": " + f['n'])
                counter = counter +1

                self.scan('Uses', f)
                #self.scan('mentions', f)
                self.scan('InstanceOf', f)
                self.scan('MemberOf', f)

        self.msg("______ count: " + str(counter))

        for s in sammler:
            self.msg("typen: " + s)

    def scan(self, t, item):
        if (t in item):
            for u in item[t]:
                self.msg("  " + t + " " + u['n'])
                if ('p' in u and str(u['p']) != 'None'):
                    self.msg("    " + u['n'] + " is a " + u['p'])
                    self.addToGraph(u['n'], RDF.type, u['p'])
                    self.addToGraph(item['n'], t, u['n'])

    def addToGraph(self, s, p, o):
        ''' insert a new triple into the graph
        :param s: Subject
        :param p: Predicate
        :param o: Object
        :return:
        '''
        if(isinstance(p, URIRef)):
            self.graph.add((self.get_onto_uriref(s), p, self.get_onto_uriref(o)))
        else:
            self.graph.add((self.get_onto_uriref(s), self.get_onto_uriref(p), self.get_onto_uriref(o)))

    def import_conceptual_data(self):
        self.msg ("import conceptual data into graph")

        self.msg ("done")

    def msg(self, txt):
        if(self.debugmode):
            print ("  " + txt)
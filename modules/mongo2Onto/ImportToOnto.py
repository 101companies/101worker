#!/usr/bin/env python3
# coding=utf-8

import os
import worker_lib

try:
    from pymongo import MongoClient
    from bson.json_util import dumps
    from bson.son import SON
except ImportError:
    print('Error: pymongo is missing: "pip3 install pymongo"')

try:
    from rdflib import ConjunctiveGraph, Graph, URIRef, BNode, Literal, RDF, Namespace
    from rdflib.plugins.serializers import turtle, n3, rdfxml
    from rdflib.store import NO_STORE, VALID_STORE
    from rdflib.namespace import FOAF, DC, RDFS
    from urllib import parse as urlparse

except ImportError:
    print('Error: rdflib is missing: "pip3 install rdflib"')

class ImportToOnto(object):

    def __init__(self, _worker_context, _graph, debug=None):
        if(debug is None):
            debug = False
        self.debugmode = debug
        self.context = _worker_context
        self.graph = _graph
        self.pageurl = "http://101companies.org/"
        if self.debugmode:
            self.pageurl = "http://localhost:3000/"

        # set references:
        self.ref_wikipage = URIRef(self.pageurl + "resource/101wikipage")
        self.ref_repo = URIRef(self.pageurl + "resource/101repo")
        self.ref_lable = URIRef("http://www.w3.org/2000/01/rdf-schema#label")
        self.ref_created = URIRef("http://purl.org/dc/terms/created")

    def prepare_graph(self):
        # 101 Vokabular einbinden
        ns101 = Namespace("https://www.101companies.org/ontology")
        self.graph.bind("101", ns101)

        # Externes Vokabular einbinden
        self.graph.bind("dc", DC)
        self.graph.bind("foaf", FOAF)

    def get_onto_uriref(self, name):
        return URIRef(self.pageurl + "resource/" + urlparse.quote(name.strip().lower()))

    def import_repo(self):
        '''
            imports the 101repo
            :return: None
            '''
        self.msg ("import repo into graph")

        self.msg ("done")

    def import_workermodules(self):
        '''
        imports the informations of 101worker and its modules based on ...
        :return: None
        '''
        self.msg ("import worker and modules into graph")

        # first, import 101worker itself:
        self.addLabel("101worker")
        self.addToGraph("101worker", FOAF.isPrimaryTopicOf, Literal("http://101companies.org/wiki/101worker"))
        #self.addToGraph("101worker", DC.abstract, Literal("Computational component of the infrastructure of the 101project"))
        self.addToGraph("101worker", URIRef('http://purl.org/dc/terms/abstract'), Literal("Computational component of the infrastructure of the 101project"))

        module_counter = 0
        for root, dirs, files in os.walk(self.context.get_env("modules101dir")):
            for file in files:
                if file.endswith("__init__.py"):
                    txt = open(os.path.join(root, file))
                    #print (txt.read().config)
                    module_counter = module_counter + 1
                    module_name = root.split('/')[-1]
                    self.msg("import module: " + module_name)
                    self.addLabel(module_name)
                    self.addToGraph(module_name, RDF.type, "101worker module")
                    self.addToGraph(module_name, DC.isPartOf, "101worker")
                    self.addToGraph(module_name, DC.requires, "101worker")
        self.msg (str(module_counter) + " modules imported")

        #msg ("Or is it " + graph.count)

        self.msg ("done")

    def import_resources_and_dumps(self):
        '''
        imports informations about resources, dumps and their relations
        :return: None
        '''
        self.msg ("import resources and dumps into graph")

        self.msg ("done")

    def import_wikipages(self):
        '''
        imports the informations given by the wiki-pages based on the wiki-links.json dump
        :return: None
        '''
        self.msg ("import wikipages into graph")
        wiki_links_json = self.context.read_dump('wiki-links')

        pages = wiki_links_json['wiki']['pages']
        types = ['Contribution',
                 'Contributor',
                 'Technology',
                 'Language',
                 'Features']

        for t in types:
            filtered  = filter(lambda p: t == p.get('p', ''), pages)
            for f in filtered:
                #self.msg('headline:' + f['headline'] + ',n:' + f['n'] + str(f))
                #self.msg(">>>>>>>>>><" + t + ": " + f['n'])

                self.addToGraph(f['n'], FOAF.isPrimaryTopicOf, Literal("http://101companies.org/wiki/" + f['p'] + ":" + f['n'].strip().replace(' ','_')))

                self.scan('Uses', f)
                #self.scan('mentions', f)
                #self.scan('LinksTo', f) # LinksTo is a wikipedia-link or mabye a github 101repo link
                self.scan('InstanceOf', f)
                self.scan('MemberOf', f)

    def import_conceptual_data(self):
        self.msg ("import conceptual data into graph")

        self.msg ("done")

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
        :return: None
        '''
        self.addLabel(s)

        if(not isinstance(o, Literal) and isinstance(o, str)):
            o = self.get_onto_uriref(o)
        if(not isinstance(p, URIRef)):
            p = self.get_onto_uriref(p)
        self.graph.add((self.get_onto_uriref(s), p, o))

    labeled_entities = []   # list of labeled entities
    def addLabel(self, item):
        '''
        insert a label of an entity if it isn't labeled
        :param item: name of the item as a string
        :return: None
        '''
        if(item not in self.labeled_entities):
            self.labeled_entities.append(item)
            self.graph.add((self.get_onto_uriref(item), DC.label, Literal(item)))

    def msg(self, txt):
        if(self.debugmode):
            print ("  " + txt)

    def test(self):
        tested_entities = []
        for s, p, o in self.graph:
            if (p == self.get_onto_uriref("instanceof")):
                if (s in tested_entities):
                    print (str(s) + " hat mehrere Instanzierungen")
                tested_entities.append(s)
        print ("anzahl: " + str(len(tested_entities)))

    def save(self, output_path, export_format):
        if (export_format == "turtle"):
            s = turtle.TurtleSerializer(self.graph)
            out = open(output_path + '.ttl', 'wb')
        elif (export_format == "xml"):
            s = rdfxml.XMLSerializer(self.graph)
            out = open(output_path + '.xml', 'wb')
        elif (export_format == "n3"):
            s = n3.N3Serializer(self.graph)
            out = open(output_path + '.n3', 'wb')
        else:
            raise Exception('unknown export format "' + export_format + '"!')
        s.serialize(out)
        self.msg('export done with format "' + export_format + '"!')

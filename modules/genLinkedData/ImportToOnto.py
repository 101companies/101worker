#!/usr/bin/env python3
# coding=utf-8

import os

from bin.worker_lib.graph import dependent_modules, depending_modules, resolve_modules_graph
from bin.worker_lib import modules

try:
    #from pymongo import MongoClient
    from bson.json_util import dumps
    from bson.son import SON
except ImportError:
    print('Error: bson is missing: "pip3 install bson"')

try:
    from rdflib import ConjunctiveGraph, Graph, URIRef, BNode, Literal, RDF, Namespace
    from rdflib.plugins.serializers import turtle, n3, rdfxml
    from rdflib.store import NO_STORE, VALID_STORE
    from rdflib.namespace import FOAF, DC, RDFS
    from urllib import parse as urlparse
except ImportError:
    print('Error: rdflib is missing: "pip3 install rdflib"')

class PrintColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class ImportToOnto(object):

    def __init__(self, _worker_context, _graph, debug = False):

        self.cur_id = 0

        self.debugmode = debug
        self.context = _worker_context
        self.graph = _graph

        self.repo_dir = self.context.get_env('repo101dir')
        self.target_dir = self.context.get_env('targets101dir')
        self.modules_dir = self.context.get_env("modules101dir")

        self.labeled_entities = []
        self.pageurl = "http://101companies.org/"
        if self.debugmode:
            self.pageurl = "http://localhost:3000/"

        self.prepare_graph()

    def prepare_graph(self):
        # bind 101 vocabulary
        ns101 = Namespace(self.pageurl + "resource/")
        self.graph.bind("ns101", ns101) # Namespace 101

        # bind externes vocabulary
        self.graph.bind("dc", DC)
        self.graph.bind("foaf", FOAF)

    def get_onto_uriref(self, name):
        name = '_'.join(name.split()).lower()

        return URIRef(self.pageurl + "resource/" + urlparse.quote(name))

    def do_import(self):
        # do collection of manuelly imports e.g. static objects
        self.do_manually_import()

        # do imports e.g. reading dumps or filestructures
        self.do_automatic_import()

    def do_manually_import(self):
        # 101 vocabulary entities
        self.addLabel("101worker")
        self.addToGraph("101worker", FOAF.isPrimaryTopicOf, Literal("http://101companies.org/wiki/101worker"), 'import_workermodules_init')
        self.addToGraph("101worker", URIRef('http://purl.org/dc/terms/abstract'), Literal("Computational component of the infrastructure of the 101project"), 'import_workermodules_init')

        self.addToGraph("uses", RDFS.comment, Literal("The subject uses the object."), 'prepare_graph')
        # legacy > self.addToGraph("instanceof", RDFS.comment, Literal("The subject is an instance of the object."), 'prepare_graph')
        self.addToGraph("memberof", RDFS.comment, Literal("The subject member the object."), 'prepare_graph')

    def do_automatic_import(self):
        self.import_wikipages()
        self.import_workermodules()
        self.import_repo()
        self.import_resources_and_dumps()
        self.import_conceptual_data()

    def import_repo(self):
        self.msg ("import repo into graph", PrintColors.OKBLUE)

        self.import_repo_bytype('technologies', 'technology')
        self.import_repo_bytype('languages', 'language')
        self.import_repo_bytype('contributions', 'contribution')

        self.msg ("done", PrintColors.OKBLUE)

    def import_repo_bytype(self, foldername, typname):
        self.msg("import from repo: " + foldername, PrintColors.ENDC, 1)
        #self.msg(self.target_dir, PrintColors.OKBLUE, 2)

        for subfolder in os.listdir(os.path.join(self.target_dir, foldername)):

            subj = self.getentityname(subfolder, typname)
            obj = self.getentityname(typname)

            self.addToGraph(subj, RDF.type, obj, 'import_repo_bytype')

            return # don't import the files yet

            # reading list of resource extentions from the current state of the ontology graph
            list_resource_ext = {}
            for s in self.graph.subjects(RDF.type, self.get_onto_uriref('resource')):
                for o in self.graph.objects(s, RDFS.label):
                    list_resource_ext.update({str(o): s})

            for root, dirs, files in os.walk(os.path.join(os.path.join(self.target_dir, foldername), subfolder)): #os.walk(self.target_dir):
                for name in files:
                    relative_resource_path = os.path.join(root, name).split(self.target_dir)[1]

                    arr_parts = relative_resource_path.split('.')
                    arr_parts.reverse()
                    resource_ext = arr_parts[1]

                    if resource_ext in list_resource_ext:
                        # print ((self.getentityname(relative_resource_path), RDF.type, list_resource_ext[resource_ext], 'import_repo_all_files'))
                        self.addToGraph(self.getentityname(relative_resource_path), RDF.type,
                                        list_resource_ext[resource_ext], 'import_repo_all_files')
                        self.addToGraph(self.getentityname(relative_resource_path), DC.isPartOf,
                                        subj, 'import_repo_all_files')

    def import_workermodules(self):
        self.msg ("import worker and modules into graph", PrintColors.OKBLUE)

        module_counter = 0
        for root, dirs, files in os.walk(self.context.get_env("modules101dir")):
            for file in files:
                if file.endswith("__init__.py"):
                    txt = open(os.path.join(root, file))

                    module_counter = module_counter + 1
                    module_name = root.split('/')[-1]

                    self.msg("import module: " + module_name, PrintColors.ENDC, 1)
                    self.addLabel(module_name)
                    self.addToGraph(module_name, RDF.type, "101worker module", 'import_workermodules')
                    self.addToGraph(module_name, DC.requires, "101worker", 'import_workermodules')
        self.msg (str(module_counter) + " modules imported", PrintColors.ENDC, 1)

        self.msg("create module dependencies", PrintColors.ENDC, 1)

        graph = resolve_modules_graph(modules)
        for module_name in graph:
            for depenting_module in depending_modules(graph, module_name):
                self.addToGraph(module_name, "depending", str(depenting_module), 'import_workermodules_dependencies')

        for module in modules:
            behavior = module.config.get('behavior')
            if behavior != None:
                for predicate in behavior:
                    for o in behavior[predicate]:
                        object_name = str(o[0] + '_' + o[1]) # e.g. dump_languagefrequency or resource_lang
                        self.addToGraph(module.__name__, 'behavior_' + predicate, object_name, 'import_workermodules_behavior')
                        self.addToGraph(object_name, RDF.type, o[0], 'import_workermodules_behavior')

                        if(str(o[0]).lower() == 'resource'):
                            self.addToGraph(object_name, URIRef('http://purl.org/dc/terms/abstract'), Literal('Is a label for naming resources like "/path/file.ext.' + o[1] + '.json"'), 'import_workermodules_behavior')
                        if(str(o[0]).lower() == 'dump'):
                            self.addToGraph(object_name, URIRef('http://purl.org/dc/terms/abstract'), Literal('Is a dump file named "' + o[1] + '.json"'), 'import_workermodules_behavior')
                        self.addLabel(object_name, o[1])

        self.msg("module dependencies added", PrintColors.ENDC, 1)

        self.msg ("done", PrintColors.OKBLUE)

    def import_resources_and_dumps(self):
        self.msg ("import resources and dumps into graph", PrintColors.OKBLUE)


        self.msg ("done", PrintColors.OKBLUE)

    def import_wikipages(self):
        self.msg ("import wikipages into graph", PrintColors.OKBLUE)
        wiki_links_json = self.context.read_dump('wiki-links')

        pages = wiki_links_json['wiki']['pages']
        types = ['Contribution',
                 'Contributor',
                 'Technology',
                 'Language',
                 'Features',
                 'Concept']

        #pagetypes = []
        #for page in pages:
        #    if page['p'] not in pagetypes:
        #        pagetypes.append(page['p'])
        #for t in pagetypes:
        #    if(t == None):
        #        t = 'none'
        #    print (t)

        for t in types:
            filtered  = filter(lambda p: t == p.get('p', ''), pages)
            for f in filtered:
                subj = self.getentityname(self.getentityname(f['n'], f['p']), 'wikipage')
                wikipage_obj = self.getentityname('101wikipage')

                self.addToGraph(subj, RDF.type, wikipage_obj, 'import_wikipages')
                self.addToGraph(subj, 'external_url', Literal("http://101companies.org/wiki/" + f['p'] + ":" + f['n'].strip().replace(' ','_')), 'import_wikipages')
                self.addToGraph(self.getentityname(f['n'], f['p']), FOAF.isPrimaryTopicOf, subj, 'import_wikipages')

                self.scan('Uses', f)
                #self.scan('mentions', f)
                #self.scan('LinksTo', f) # LinksTo is a wikipedia-link or mabye a github 101repo link
                self.scan('MemberOf', f)
                self.scan('PartOf', f)
                self.scan('InstanceOf', f, RDF.type)  # alternative predicate because InstanceOf is legacy

        self.msg ("done", PrintColors.OKBLUE)

    def scan(self, t, item, alt_predicate = None):
        if (t in item):
            for u in item[t]:
                #self.msg("  " + t + " " + u['n'])

                #if ('p' in u and u['p'] != None):

                subj = self.getentityname(u['n'], u['p']) # e.g. language-haskell
                item_name = self.getentityname(item['n'], item['p'])

                if u['p'] != None:
                    subj_type = self.getentityname(u['p'])  # , 'namespace') # e.g. namespace-language
                    item_type = self.getentityname(item['p'])#, 'namespace')
                    #self.addToGraph(subj, RDF.type, subj_type, 'scan_' + t + '1')
                    self.addToGraph(item_name, RDF.type, item_type, 'scan_' + t + '2')

                    if u['p'].lower() == 'namespace':
                        subj = self.getentityname(u['n'])

                self.addLabel(subj, u['n']) # e.g. Label "Haskell" for Entity language-haskell

                if alt_predicate != None:
                    self.addToGraph(item_name, RDF.type, subj, 'scan_' + t + '3')
                else:
                    self.addToGraph(item_name, t.lower(), subj, 'scan_' + t + '3')

    def import_conceptual_data(self):
        self.msg ("import conceptual data into graph", PrintColors.OKBLUE)

        self.msg ("done", PrintColors.OKBLUE)

    def getentityname(self, subjname, typename = None):

        if(typename):
            return typename.lower() + "-" + subjname.lower()
        else:
            return subjname.lower()

    def addToGraph(self, s, p, o, debuginfo):

        s = self.get_onto_uriref(s)

        if (self.debugmode):
            self.graph.add(
                (s,
                 self.get_onto_uriref('importedBy'),
                 self.get_onto_uriref(debuginfo))
            )
            self.graph.add(
                (self.get_onto_uriref(debuginfo),
                 RDF.type,
                 self.get_onto_uriref('import_method'))
            )
            self.graph.add(
                (self.get_onto_uriref(debuginfo),
                 DC.isPartOf,
                 self.get_onto_uriref('genLinkedData'))
            )

        if(not isinstance(o, Literal) and not isinstance(o, URIRef) and isinstance(o, str)):
            o = self.get_onto_uriref(o)
        if not isinstance(p, URIRef):
            p = self.get_onto_uriref(p)

        # Add tuple to graph
        self.graph.add((s, p, o))

        #if p == RDF.type and 'namespace' not in o and 'langua' in o:
        #    print ((s,p,o, debuginfo))

        if self.debugmode:
            id_uri_ref = self.get_onto_uriref('ontology_data_id')
            id_exists = False
            for id in self.graph.objects(s, id_uri_ref):
                id_exists = True
            for id in self.graph.objects(o, id_uri_ref):
                id_exists = True

            if not id_exists:
                self.cur_id += 1
                self.graph.add((s, id_uri_ref, Literal(self.cur_id)))
                if not isinstance(o, Literal):
                    self.graph.add((o, id_uri_ref, Literal(self.cur_id)))

    def addLabel(self, entity, label = None):

        if label == None:
            label = entity

        if(entity not in self.labeled_entities):
            self.labeled_entities.append(entity)
            self.graph.add((self.get_onto_uriref(entity), RDFS.label, Literal(label)))

    def msg(self, txt, txtcolor = PrintColors.ENDC, level = 0):
        if(self.debugmode):
            print (txtcolor + ('  ' * (level + 1)) + txt + PrintColors.ENDC)

    def check_integrity(self):
        self.msg("checking integrity now", PrintColors.OKBLUE)

        # Recognize similar objects

        # check predicates, which are to be used once
        single_use_predicats = [
            RDFS.label,
            URIRef('http://purl.org/dc/terms/abstract')
        ]

        if False:
            # insert wrong data
            for p in single_use_predicats:
                self.addToGraph('test', p, 'a', 'check_integrity')
                self.addToGraph('test', p, 'b', 'check_integrity')

        checked_subjects = []
        for s in self.graph.subjects():
            if s not in checked_subjects:
                checked_subjects.append(s)
                for pred in single_use_predicats:
                    tmp = []
                    for o in self.graph.objects(s, pred):
                        if(o not in tmp):
                            tmp.append(o)
                            if (len(tmp) == 2):
                                self.msg(str(s) + ' has multiple ' + str(pred) + "(" + str(o), PrintColors.WARNING, 1)

        self.msg("done", PrintColors.OKBLUE)

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

        self.msg('export done in format "' + export_format + '"', PrintColors.OKGREEN)

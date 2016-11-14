#!/usr/bin/env python3
# coding=utf-8

from .ImportToOnto import *

import time
import requests

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': False
}

def createRDFGraph(context):
    graphfilepath = get_output(context)

    # load graph
    graph = Graph()
    graph.open(get_output(context), create=False)

    # 101onto erzeugen:
    # 1. rdfs laden
    # 2. dem rdfs entsprechend die 101 relationen erzeugen
    # 3. als ontology speichern
    # 4.1 für den import wieder laden
    # 4.2 im Import korrekte links verwenden

    # import 101companies
    ito = ImportToOnto(context, graph, True)
    ito.do_import()

    ito.check_integrity()
    #ito.test()

    #ito.viz()

    # export graph
    #export_format = "xml"
    #export_format = "turtle"
    # export_format = "n3"
    # export_format = "pretty-xml"
    #ito.save(graphfilepath, export_format)

    ito.save(graphfilepath, "turtle")
    ito.save(graphfilepath, "xml")
    ito.save(graphfilepath, "n3")
    #ito.save(graphfilepath, "foo")

#def createSingleFiles(context):
    graphfilepath = get_output(context)

    # Graphen laden
    #graph = g.Graph()
    #graph.parse(get_output(context))

    #print(len(graph))
    #import pprint
    #for stmt in graph:
    #    pprint.pprint(stmt)

    #for subject,predicate,obj_ in graph:
    #    print (subject + ' ' + predicate + ' ' . obj_)


def get_output(context):
    return os.path.join(context.get_env('ontoDir'), 'ontology')

def run(context):
    start_time = time.time()

    createRDFGraph(context)

    print("--- %s ms ---" % ((time.time() - start_time)*1000))

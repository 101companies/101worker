#!/usr/bin/env python3
# coding=utf-8

from .ImportToOnto import *
import time

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

    # import 101companies
    ito = ImportToOnto(context, graph, False)
    ito.import_wikipages()
    ito.import_workermodules()
    ito.import_repo()
    ito.import_resources_and_dumps()
    ito.import_conceptual_data()

    ito.test()

    # export graph
    export_format = "xml"
    #export_format = "turtle"
    #export_format = "pretty-xml"
    graph.serialize(destination=graphfilepath, format=export_format)

def createSingleFiles(context):
    graphfilepath = get_output(context)

    # Graphen laden
    graph = g.Graph()
    graph.parse(get_output(context))

    print(len(graph))
    import pprint
    for stmt in graph:
        pprint.pprint(stmt)

    for subject,predicate,obj_ in graph:
        print (subject + ' ' + predicate + ' ' . obj_)


def get_output(context):
    return os.path.join(context.get_env('ontoDir'), 'ontology')

def run(context):
    start_time = time.time()

    createRDFGraph(context)

    print("--- %s ms ---" % ((time.time() - start_time)*1000))

    #createSingleFiles(context)

#!/usr/bin/env python3
# coding=utf-8

from .ImportToOnto import *

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': False
}

def createRDFGraph(context):
    export_format = "xml"
    export_format = "turtle"
    #export_format = "pretty-xml"
    graphfilepath = get_output(context)

    # Graphen laden
    graph = g.Graph()
    graph.open(get_output(context), create=False)

    # Externes Vokabular einbinden
    ns101 = Namespace("https://www.w3.org/TR/rdf-syntax-grammar/")

    graph.bind("101", ns101)
    graph.bind("dc", DC)
    graph.bind("foaf", FOAF)

    ito = ImportToOnto(context, graph)

    ito.import_repo()
    ito.import_workermodules()
    ito.import_resources_and_dumps()
    ito.import_wikipages()
    ito.import_conceptual_data()

    # Graphen exportieren
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
        msg(subject + ' ' + predicate + ' ' . obj_)


def get_output(context):
    return os.path.join(context.get_env('ontoDir'), 'ontology')

def run(context):
    createRDFGraph(context)
    #createSingleFiles(context)

''' Kann das weg?:
if __name__ == '__main__':
    main()
'''
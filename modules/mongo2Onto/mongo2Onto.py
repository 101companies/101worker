#!/usr/bin/env python3
# coding=utf-8

from .graph_imports import *

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': False
}

def createRDFGraph(context):
    export_format = "xml"
    #export_format = "turtle"
    #export_format = "pretty-xml"
    graphfilepath = get_output(context)

    # Graphen laden
    graph = g.Graph()
    graph.open(get_output(context), create=False)

    # Externes Vokabular einbinden
    graph.bind("dc", DC)
    graph.bind("foaf", FOAF)

    import_repo(context, graph)
    import_workermodules(context, graph)
    import_resources_and_dumps(context, graph)
    import_wikipages(context, graph)
    import_conceptual_data(context, graph)

    # Graphen exportieren
    graph.serialize(destination=graphfilepath, format=export_format)

def get_output(context):
    return os.path.join(context.get_env('ontoDir'), 'ontology')

def run(context):
    createRDFGraph(context)
    print ("done")

''' Kann das weg?:
if __name__ == '__main__':
    main()
'''
import networkx as nx

def resolve_modules_graph(modules):
    settings = {}

    for module in modules:
        behavior = module.config.get('behavior')
        if behavior:
            settings[module] = behavior

    # create a mapping which module produces which resources
    creations = {}
    for module, behavior in settings.items():
        for creates in behavior.get('creates', []):
            creations[creates[0] + ':' + creates[1]] =  module

    # create a mapping for module depending on other module by resource
    # data is { module: [module_creating_the_resource, resource_name], ... }
    deps = {}
    for module, behavior in settings.items():
        if behavior.get('uses', []):
            deps[module] = []
        for uses in behavior.get('uses', []):
            name = uses[0] + ':' + uses[1]
            deps[module] += [[creations[name], name]]

    graph = nx.DiGraph()

    for module in modules:
        graph.add_node(module.__name__)
    for dep, data in deps.items():
        for [source, name] in data:
            graph.add_edge(dep.__name__, source.__name__, label=name)

    return graph

def dependent_modules(graph, name):
    return nx.ancestors(graph, name)

def depending_modules(graph, name):
    return nx.descendants(graph, name)

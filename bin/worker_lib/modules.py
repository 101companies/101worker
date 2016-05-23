import importlib
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../modules')))

def import_module(module_name):
    return importlib.import_module(module_name)

modules = [
    'pull',
    'matchLanguage',
    'extractFacts',
    'dumpMongoDBToJson',
    'convertMongoDump',
    'simpleLOC',
    'locPerContribution',
    'wiki2tagclouds',
    'moretagclouds',
    'zip'
]

modules = [import_module(module) for module in modules]

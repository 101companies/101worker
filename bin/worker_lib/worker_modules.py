import importlib
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../modules')))

def import_module(module_name):
    return importlib.import_module(module_name)

module_names = [
    'pull',
    'matchLanguage',
    'extractFacts',
    'dumpPG',
    'convertMongoDump',
    'packageFrequency',
    'languageFrequency',
    'simpleLOC',
    'locPerContribution',
    'wiki2tagclouds',
    'moretagclouds',
    'plainTextWikiDump',
    'genLinkedData',
    'zip'
]

worker_modules = [import_module(module) for module in module_names]

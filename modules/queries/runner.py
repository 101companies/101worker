__author__ = 'avaranovich'

import json
import os
from connection import Connection
from jinja2 import Environment, FileSystemLoader

if __name__=='__main__':
    env = Environment(loader=FileSystemLoader('tmpl'))
    connection = Connection('http://triples.101companies.org/openrdf-sesame/')
    connection.use_repository('Testing_2')

    connection.addnamespace('onto', 'http://101companies.org/ontology#')
    connection.addnamespace('res', 'http://101companies.org/resources#')

    relevant_path = os.path.join(os.path.dirname(__file__), 'specs')
    included_extenstions = ['json']
    file_names = [fn for fn in os.listdir(relevant_path) if any([fn.endswith(ext) for ext in included_extenstions])]

    for file in file_names:
        js = json.load(open(os.path.join(os.path.dirname(__file__), 'specs', file)))
        query_file = js['query']
        if query_file == '':
            continue
        print query_file
        with open(os.path.join(os.path.dirname(__file__), 'sparql', query_file)) as f:
            query = f.read()
            #print query
            res = connection.query(query)
            print res

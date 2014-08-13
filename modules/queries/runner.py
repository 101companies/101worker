__author__ = 'avaranovich'

import json
import os
from connection import Connection
from jinja2 import Environment, FileSystemLoader

if __name__=='__main__':
    env = Environment(loader=FileSystemLoader('templates'))
    connection = Connection('http://triples.101companies.org/openrdf-sesame/')
    connection.use_repository('Testing_2')

    connection.addnamespace('onto', 'http://101companies.org/ontology#')
    connection.addnamespace('res', 'http://101companies.org/resources#')

    relevant_path = os.path.join(os.path.dirname(__file__), 'sparql')
    included_extenstions = ['sparql']
    file_names = [fn for fn in os.listdir(relevant_path) if any([fn.endswith(ext) for ext in included_extenstions])]

    for query_file in file_names:
        template_file = query_file.replace('sparql', 'tmpl')
        if query_file == '' or template_file == '':
            continue
        print query_file
        with open(os.path.join(os.path.dirname(__file__), 'sparql', query_file)) as f:
            query = f.read()
            #print query
            if query_file == "baselineContribution.sparql":
                infer = False
            else:
                infer = True

            if not infer:
                res = connection.query(query, inference=False)
            else:
                res = connection.query(query)

            print res


            file_to_save = template_file
            if not os.path.isfile(os.path.join(os.path.dirname(__file__), 'templates', template_file)):
                template_file = "default.tmpl"

            template = env.get_template(template_file)
            output = template.render(data=res)
            #print output

            with open(os.path.join(os.path.dirname(__file__), 'output', file_to_save.replace('.tmpl', '.txt')), "w") as output_file:
                output_file.write(output)

            #print res

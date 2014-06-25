__author__ = 'avaranovich'

import json
from connection import Connection
from jinja2 import Environment, FileSystemLoader


class Entity:
    def __init__(self, fn):
        json_data = open(fn)
        data = json.load(json_data)

        self.context = data['@context']
        if 'properties' in data:
            self.properties = data['properties']
        else:
            self.properties = None

        self.id = data['@id']
        self.type = data['@type']

        self.env = Environment(loader=FileSystemLoader('tmpl'))
        self.connection = Connection('http://triples.101companies.org/openrdf-sesame/')
        self.connection.use_repository('ML_testing')

        self.connection.addnamespace('onto', 'http://101companies.org/ontology#')
        self.connection.addnamespace('res', 'http://101companies.org/resources#')

    def checkCardinality(self):
        template = self.env.get_template('cardinalityCheck')
        type = self.id

        if self.properties is None:
            return

        for prop in self.properties:
            p = prop['property']
            c = prop['minCardinality']
            print "Cardinality check for class: %s and relationship: %s" % (type, p)
            query = template.render(ontoClass=type, relationship=p)
            res2 = self.connection.query(query)
            for r in res2:
                print ">># of relationships declared: %s" % r['count']['value']
                if int(r['count']['value']) > 0:
                    #print r
                    print r['x']['value']


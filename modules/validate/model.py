__author__ = 'avaranovich'

import json
from connection import Connection
from jinja2 import Environment, FileSystemLoader

class Entity:
    def __init__(self, fn):
        json_data = open(fn)
        data = json.load(json_data)

        #self.context = data['@context']
        if 'properties' in data:
            self.properties = data['properties']
        else:
            self.properties = None

        self.id = data['@id']
        self.type = data['@type']

        self.env = Environment(loader=FileSystemLoader('tmpl'))
        self.connection = Connection('http://triples.101companies.org/openrdf-sesame/')
        self.connection.use_repository('Testing_2')

        self.connection.addnamespace('onto', 'http://101companies.org/ontology#')
        self.connection.addnamespace('res', 'http://101companies.org/resources#')

    def checkCardinality(self):
        template = self.env.get_template('cardinalityCheck')
        type = self.id

        if self.properties is None:
            return

        for prop in self.properties:
            p = prop['property']
            c = int(prop['minCardinality'])
            print "Cardinality check for class: %s and relationship: %s" % (type, p)
            query = template.render(ontoClass=type, relationship=p)
            res2 = self.connection.query(query)
            for r in res2:
                #print ">># of relationships declared: %s" % r['count']['value']
                if int(r['count']['value']) > 0:
                    #print r
                    #print r['count']['value']
                    v = int(r['count']['value'])
                    if v < c:
                        print "ERROR"

    @staticmethod
    def checkHirerarchy():
        env = Environment(loader=FileSystemLoader('tmpl'))
        connection = Connection('http://triples.101companies.org/openrdf-sesame/')
        connection.use_repository('Testing_2')

        connection.addnamespace('onto', 'http://101companies.org/ontology#')
        connection.addnamespace('res', 'http://101companies.org/resources#')
        template = env.get_template('subtypeCheck')
        print "Subtyping check"
        query = template.render()
        res = connection.query(query)
        x = list()
        for r in res:
            print r
            if not r.has_key('c'):
                t = ("Base: " + r['a']['value'], "First Child: " + r['b']['value'])
            else:
                t = ("Base: " + r['a']['value'], "First Child: " + r['b']['value'], "Second Child: " + r['c']['value'])
            if not t in x:
                x.append(t)
        print x
        with open('subtyping_errors.json', 'w') as outfile:
            json.dump(x, outfile)
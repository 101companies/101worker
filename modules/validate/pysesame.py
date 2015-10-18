#borrowed from https://github.com/rahuldave/semflow/blob/master/pysesame.py

import os
from urllib import quote_plus, urlencode, quote
import urllib2, types
import json as simplejson
from json import loads
from jinja2 import Environment, FileSystemLoader
from model import Entity
from connection import Connection

#get all features that are implemented by a contribution, but don't declared as of type Feature
wrongTypes="""
SELECT * WHERE {
  {
   ?contribution rdf:type onto:Contribution .
   ?contribution onto:implements ?feature .
  }
  MINUS
  {
   ?contribution rdf:type onto:Contribution.
   ?contribution onto:implements ?feature.
   ?feature rdf:type onto:Feature .
  }
}
"""

# property must be declared, but it is not declared
contribWithoutFeaturesDeclared="""
SELECT DISTINCT ?contribution WHERE {
  ?contribution rdf:type onto:Contribution .
  { FILTER NOT EXISTS { ?contribution onto:implements ?feature . } }
}
"""

contribWithoutFeaturesImplemented="""
SELECT DISTINCT ?contribution (COUNT(?feature) AS ?featureCount) WHERE {
  ?contribution rdf:type onto:Contribution .
  ?contribution onto:implements ?feature .
} GROUP BY ?contribution
"""

def typeCheck(env, ontoClassX, ontoClassY, relationship):
    print "Type check for: %s %s %s" % (ontoClassX, relationship, ontoClassY)
    template = env.get_template('typeCheck')
    query = template.render(ontoClassX=ontoClassX, ontoClassY=ontoClassY, relationship=relationship)
    res = c.query(query)
    print "Wrong types:"
    for r in res:
        print ">>", r['y']['value'], "detected in", r['x']['value']


if __name__=='__main__':
    with open("models", "r") as ins:
        modelsPath = ins.read().splitlines()[0]

    included_extenstions = ['json']
    file_names = [fn for fn in os.listdir(modelsPath) if any([fn.endswith(ext) for ext in included_extenstions])]

    for file in file_names:
        entity = Entity(os.path.abspath(os.path.join(modelsPath, file).replace("\\","/")))
        #The check below is a special case of the cardinality check, so it's not needed
        #entity.checkRelationsExistance()
        entity.checkCardinality()
        entity.checkHirerarchy()

    env = Environment(loader=FileSystemLoader('tmpl'))
    c = Connection('http://triples.101companies.org:8080/openrdf-sesame/')
    c.use_repository('sandbox')

    c.addnamespace('onto', 'http://101companies.org/ontology#')
    c.addnamespace('res', 'http://101companies.org/resources#')

    #existanceCheck(env, 'Contribution', 'implements')
    #cardinalityCheck(env, 'Contribution', 'implements')
    typeCheck(env, 'Contribution', 'Feature', 'implements')

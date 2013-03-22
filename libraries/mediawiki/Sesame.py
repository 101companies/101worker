from urllib2 import urlopen, Request
import urllib
import json


# Class that can be used to query the Sesame Triplestore of the Wiki
class Store:
    def __init__(self, endpointUrl='http://sl-mac.uni-koblenz.de:8081/openrdf-sesame', repository='wiki101'):
        """
        Inits the class with some basic values
        :param endpointUrl: The URL of the endpoint (preset to the 101companies Sesame RDF store
        :param repository: The repository which is to be queried (preset to the wiki repository)
        """
        self.url = '{0}/repositories/{1}'.format(endpointUrl, repository)


    def select(self, query):
        """
        Executes a select query for the Sesame TripleStore.
        Example Query: SELECT * WHERE { ?subject ?predicate ?object . }
        Since Sesame uses a REST approach, this method will create a GET request

        :param query: The query that should be executed
        :return: The result as a Python dictionary
        """
        tUrl = self.url
        if not tUrl.endswith('?'):
            tUrl += "?"
        tUrl += 'query={0}'.format(urllib.quote(query.replace('\n', ' ')))

        req = Request(tUrl)
        req.add_header('accept', 'application/sparql-results+json')

        res = urlopen(req).read()

        return json.loads(res)


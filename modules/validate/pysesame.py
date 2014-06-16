#borrowed from https://github.com/rahuldave/semflow/blob/master/pysesame.py

from urllib import quote_plus, urlencode, quote
import urllib2, types
import json as simplejson
from json import loads
from jinja2 import Environment, FileSystemLoader

SPJSON='application/sparql-results+json'
SPXML='application/sparql-results+xml'
SPCXML='application/rdf+xml'
SPCN3='text/rdf+n3'
SPATXT='text/boolean'

SPOC={
    's':'subj',
    'o':'obj',
    'p':'pred',
    'c':'context'
}

class connection:
    def __init__(self,url):
        self.baseurl=url
        self.sparql_prefix=""
    
    def addnamespace(self,id,ns):
        self.sparql_prefix+='PREFIX %s:<%s>\n' % (id,ns) 
    
    def __getsparql__(self, atype, method, uri=None):
        """Updated to support both POST and get styles. If POST, the posting 
        uri must be supplied. If GET method is entire URI, if POST its the 
        query string
        """
        #print method,uri
        if uri!=None:
            req=urllib2.Request(self.baseurl+uri)
        else:
            req=urllib2.Request(self.baseurl+method)
        req.add_header('Accept', atype)
        req.add_header('Accept', 'application/sparql-results+json')
        #NEEDED to SET above to get sensible results.
        #req.add_header('Accept', 'application/rdf+xml')
        #req.add_header('Accept', 'application/sparql-results+xml')
        if uri !=None:
            req.add_data(method)
            req.add_header('Content-Type','application/x-www-form-urlencoded')
            #print "INPUTDATA", req.get_data()
        try:
            sock=urllib2.urlopen(req)
            #print "INFO", sock.info()
            data=sock.read()
            #print "DATA", data
            sock.close()
        except urllib2.HTTPError, e:
            print 'Code: ', e.code
        except urllib2.URLError, e:
            print 'Reason: ', e.reason
        except:
            import sys, traceback
            data=""
            print "ERROR", traceback.print_tb(sys.exc_info()[2])
            #return [{'error':data}]
        if atype != SPJSON:
            print "ATYPE", atype
            return data
        try:
            #print "LOADSDATA", data
            result=loads(data)['results']['bindings']
            return result
        except:
            import sys, traceback
            print "ERRORX", traceback.print_tb(sys.exc_info()[2])
            return [{'error':data}]
        
    def use_repository(self,r):
        self.repository=r
    
    def query(self,q, atype=SPJSON):
        #print "LENGTH", len(self.sparql_prefix+q)
        q='repositories/'+self.repository+'?query='+quote_plus(self.sparql_prefix+q)
        #print "Q",q
        return self.__getsparql__(atype, q)
        
    def querypost(self, q, atype=SPJSON):
        uri='repositories/'+self.repository
        #print self.sparql_prefix
        #print q
        q='query='+quote_plus(self.sparql_prefix+q)
        #print q
        #q='query='+quote_plus(q)
        
        #print "Q",q
        return self.__getsparql__(atype, q, uri)
        
    def construct_query(self,q):
        q='repositories/'+self.repository+'?query='+quote_plus(self.sparql_prefix+q)
        res=urllib2.urlopen(self.baseurl+q)
        data=res.read()
        res.close()
        return data
    
    def query_statements(self, qdict, atype=SPCXML):
        "query statements in rep for subject, object, predicate, or context..spoc"
        host=self.baseurl+'repositories/'+self.repository+'/statements'
        #print 'HOST', host 
        #BUG we do not handle if qitem is a list yet
        qlist=[]
        for qtype, qitem in qdict.items():
            if type(qitem)==types.ListType:#NOT SUPPORTED BY SESAME
                for themem in qitem:
                    qlist.append(SPOC[qtype]+"="+quote_plus(themem))
            else:
                qlist.append(SPOC[qtype]+"="+quote_plus(qitem))
        endpoint=host+"?"+'&'.join(qlist) 
        #print "ENDPOINT",endpoint
        req=urllib2.Request(endpoint)
        #accepting rdf/xml not ntriples
        req.add_header('Accept', atype)
        res=urllib2.urlopen(req)
        #print "INFO", res.info()
        readstuff=res.read()
        res.close()
        return readstuff
        
    def get_in_context(self, context=None, atype=SPCXML):
        host=self.baseurl+'repositories/'+self.repository+'/statements'
        if context==None:
            endpoint=host
        else:
            endpoint=host+"?"+'context='+quote_plus(context) 
        #print "ENDPOINT",endpoint
        req=urllib2.Request(endpoint)
        #accepting rdf/xml not ntriples
        req.add_header('Accept', atype)
        res=urllib2.urlopen(req)
        #print "INFO", res.info()
        readstuff=res.read()
        res.close()
        return readstuff
    
    def deletedata(self, context=None):
        #delete everything in a repository or in a specific context
        host=self.baseurl+'repositories/'+self.repository+'/statements'
        if context==None:
            endpoint=host
        else:
            endpoint=host+"?"+'context='+quote_plus(context)
        #print 'HOST', host , endpoint
        req=urllib2.Request(endpoint)
        req.get_method = lambda: 'DELETE'
        try:
            res=urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print 'Code: ', e.code
            res=None
            if e.code > 299:
                print 'Error code: ', e.code
                raise ValueError(e.code)
            res.close()
            return 0
        #print "INFO", res.info()
        res.close()
        return 0
           
    def postdata(self,data, context=None, method='POST'):
        "POST/PUT a bunch of RDF statements into the repository"
        #PUT replaces, rather than adds, either for whole rep, or for context
        #/openrdf-sesame/repositories/mem-rdf/statements
        host=self.baseurl+'repositories/'+self.repository+'/statements'
        if context==None:
            endpoint=host
        elif type(context)==types.ListType:
            qlist=["context="+ele for ele in context]
            endpoint=host+"?"+'&'.join(qlist)
        else:
            endpoint=host+"?"+'context='+context
        #print 'ENDPOINT', endpoint 
        req=urllib2.Request(endpoint)
        if method=='PUT':#otherwise assume POST
            req.get_method = lambda: 'PUT'
        req.add_header('Content-Type', SPCXML)
        req.add_data(data)
        try:
            res=urllib2.urlopen(req)
            print res.info()
        except urllib2.HTTPError, e:
            print 'Code: ', e.code
            res=None
            if e.code > 299:
                print 'Error code: ', e.code
                raise ValueError(e.code)
            res.close()
            return 0
        #print "INFO", res.info()
        #readstuff=res.read()
        res.close()
        return 0
       
    def postfile(self, thefile, context=None, method='POST'):
        #print "FILE", thefile
        fd=open(thefile)
        data=fd.read()
        fd.close()
        #print "DATA"
        #print data
        #print "========================"
        res=self.postdata(data, context, method)
        return res	

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

def cardinalityCheck(env, ontoClass, relationship):
    print "Cardinality check for class: %s and relationship: %s" % (ontoClass, relationship)
    template = env.get_template('cardinalityCheck')
    query = template.render(ontoClass=ontoClass, relationship=relationship)
    res2 = c.query(query)
    for r in res2:
        print ">># of relationships declared: %s" % r['count']['value']

def typeCheck(env, ontoClassX, ontoClassY, relationship):
    print "Type check for: %s %s %s" % (ontoClassX, relationship, ontoClassY)
    template = env.get_template('typeCheck')
    query = template.render(ontoClassX=ontoClassX, ontoClassY=ontoClassY, relationship=relationship)
    res = c.query(query)
    print "Wrong types:"
    for r in res:
        print ">>", r['y']['value'], "detected in", r['x']['value']

def existanceCheck(env, ontoClass, relationship):
    print "Existence check"
    template = env.get_template('existenceCheck')
    query = template.render(ontoClass=ontoClass, relationship=relationship)
    res1 = c.query(query)
    for r in res1:
        print ">>", r

if __name__=='__main__':

    env = Environment(loader=FileSystemLoader('tmpl'))
    c = connection('http://triples.101companies.org/openrdf-sesame/')
    c.use_repository('ML_testing')

    c.addnamespace('onto', 'http://101companies.org/ontology#')
    c.addnamespace('res', 'http://101companies.org/resources#')

    existanceCheck(env, 'Contribution', 'implements')
    cardinalityCheck(env, 'Contribution', 'implements')
    typeCheck(env, 'Contribution', 'Feature', 'implements')

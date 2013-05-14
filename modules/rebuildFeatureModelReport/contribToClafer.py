import sys
import urllib
import urllib2
import json
import re

def featureURLToClafer(url):
	raw = re.sub("http://101companies.org/resource/Feature-3A","", url)
	return re.sub("([a-zA-Z])\_([a-zA-Z])",lambda pat: pat.group(1) + pat.group(2).upper(), raw)

def contribToClafer(contrib):
  host = "http://triples.101companies.org"
  port = "80"
  service = "org.softlang.semanticendpoint/doQuery"
  parameters = {"method" : "getResourceTriples", "resource" : "Contribution-3A" + contrib}
  url = "%s:%s/%s?%s" % (host, port, service, urllib.urlencode(parameters))
  triples = json.loads(urllib2.urlopen(url).read().replace("callback(","").replace(")",""))
  featureTriples = filter(lambda t : t['predicate'] == "http://101companies.org/property/implements", triples)
  claferFeatures = map(lambda t : featureURLToClafer(t['node']), featureTriples)
  output = contrib.title() + " : FeatureSpec\n\t ["
  if not claferFeatures:
    raise Exception("No implemented features specified.")
  output +=  '\n\t  '.join(cf for cf in claferFeatures)
  output += "]"
  return output


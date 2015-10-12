import urllib
import urllib2
import json
import re

def urlToClafer(url, prefix):
  return urlNameToClafer(urlTourlName(url, prefix))

def urlTourlName(url, suffix):
  return re.sub("http://101companies.org/resource/" + suffix ,"", url)

def urlNameToClafer(url):
  raw = re.sub('-2D', '_', url)
  return re.sub("([a-zA-Z])\_([a-zA-Z])",lambda pat: pat.group(1) + pat.group(2).upper(), raw)

def load(resourcename):
  host = "http://triples.101companies.org"
  port = "80"
  service = "org.softlang.semanticendpoint/doQuery"
  parameters = {"method" : "getResourceTriples", "resource" : resourcename}
  url = "%s:%s/%s?%s" % (host, port, service, urllib.urlencode(parameters))
  return json.loads(urllib2.urlopen(url).read().replace("callback(","").replace(")",""))

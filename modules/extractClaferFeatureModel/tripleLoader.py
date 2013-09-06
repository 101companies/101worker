import urllib
import urllib2
import json
import re

def urlTourlName(url, suffix):
  return re.sub("http://101companies.org/resource/" + suffix ,"", url)

def urlNameToClafer(url):
  raw = re.sub('-2D', '_', url)
  raw = re.sub(' ', '_', raw)
  raw = re.sub('-', '_', raw)
  return re.sub("([a-zA-Z])\_([a-zA-Z])",lambda pat: pat.group(1) + pat.group(2).upper(), raw)

def load(resourcename):
  url = "http://101companies.org/endpoint/" + resourcename + "/json/directions"
  return json.loads(urllib2.urlopen(url).read().replace("callback(","").replace(")",""))

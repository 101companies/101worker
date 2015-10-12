import json
import urllib2
from triple import Triple
import inflect
p = inflect.engine()
from termcolor import colored

class WikiResource:
  def __init__(self, ns = "", rtitle = "", urinotation = "", load = False):
    if urinotation:
      split = urinotation.split("/")
      singular = p.singular_noun(split[0])
      if singular:
        ns = singular.capitalize()
      else:
        ns = split[0].capitalize()
      rtitle = "/".join(split[1:])
    self.ns = ns
    self.rtitle = rtitle
    self.title = self.ns + ":" + self.rtitle
    if load:
      print "Loading resource " + str(self)
      self.gettriples()
      self.getdata()
    else:
      self.triples = []
      self.data = dict()

  def __str__(self):
    return colored(self.title, 'green')

  def backlinks(self):
    return self.data['backlinks']

  def getdata(self):
    apiurl = "http://101companies.org/api/pages/" + self.ns + ":" + self.rtitle
    self.data = json.load(urllib2.urlopen(apiurl.replace(" ", "%20")))

  def gettriples(self):
    tripleurl = "http://101companies.org/endpoint/" + self.ns + ":" + self.rtitle + "/json"
    print tripleurl.replace(" ", "%20")
    self.triples = map(Triple, json.load(urllib2.urlopen(tripleurl.replace(" ", "%20"))))


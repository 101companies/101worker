from wikiResource import WikiResource
import json
import urllib2
import sys
import os
import re
import unicodedata
from termcolor import colored

class Contribution(WikiResource):

  def __init__(self, title, commitsha=None, loadfeatures=False):
    self.commitsha = commitsha
    self.title = title
    WikiResource.__init__(self, "Contribution", title, load = True)
    self.rooturl = "http://101companies.org/resources/contributions/"
    self.baseresourceurl = self.rooturl + self.rtitle
    self.getFeatures()
    if loadfeatures:
      self.getLocations()

  # http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
  def slugify(self,value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

  def aggregate(self,path):
    simplepath = path.replace(self.rooturl, '')
    print "Operating in " + colored(simplepath, 'blue')
    rawdata = urllib2.urlopen(path)
    data = json.load(rawdata)
    if 'folders' in data:
      for feature in self.features:
        candidates = filter(lambda f: feature.lower() in f['name'].lower(), data['files'])
        for c in candidates:
          print " > Checking " + colored(c['classifier'] + ':' + c['name'] , 'cyan')
          self.features[feature] = filter(lambda r:  r['resource'] not in c['resource'],self.features[feature])
        self.features[feature].extend(candidates)
      for folder in data['folders'] + data['files']:
        self.aggregate(folder['resource'])
    else:
      for feature in self.features:
        candidates = filter(lambda f: feature.lower() in f['name'].lower(), data['fragments'])
        for c in candidates:
          print " > Checking " + colored(c['name'], 'cyan') + ' (' + colored(c['classifier'] , 'cyan') + ')'
          self.features[feature] = filter(lambda r: r['resource'] not in c['resource'], self.features[feature])
        self.features[feature].extend(candidates)


  def getLocations(self):
    self.aggregate(self.baseresourceurl)

  def getFeatures(self):
    ctriples = filter(lambda x: x.toInternal and x.predicate == "implements" and x.object.ns == "Feature" ,self.triples)
    self.features = {}
    for ctriple in ctriples:
      self.features[ctriple.object.rtitle] = []

from wikiResource import WikiResource
import json
import urllib2
import sys
import os
import re
import unicodedata
from termcolor import colored

class Contribution(WikiResource):

  def __init__(self, title, rules, commitsha=None, loadfeatures=False):
    self.commitsha = commitsha
    self.title = title
    WikiResource.__init__(self, "Contribution", title, load = True)
    self.rooturl = "http://101companies.org/resources/contributions/"
    self.baseresourceurl = self.rooturl + self.rtitle
    self.features = {}
    for feature_name in rules.keys():
      self.features[feature_name] = []
    self.rules = rules
    if loadfeatures:
      self.getLocations()

  # http://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename-in-python
  def slugify(self,value):
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

  def pattern_matches(self, pattern, keywords, fragment_name):
    if pattern == 'prefix':
      return any(map(lambda keyword: fragment_name.lower().startswith(keyword.lower()), keywords))
    elif pattern == 'postfix':
      return any(map(lambda keyword: fragment_name.lower().endswith(keyword.lower()), keywords))
    elif pattern == 'any':
      return any(map(lambda keyword: keyword.lower() in fragment_name.lower(), keywords))
    elif pattern == 'exact':
      return any(map(lambda keyword: keyword.lower() == fragment_name.lower(), keywords))
    return False


  def is_candidate(self, fragment, feature_name):
    feature_level = self.rules[feature_name]
    language_level = None
    if 'Haskell' in feature_level:
      language_level = feature_level['Haskell']
    elif '*' in feature_level:
      language_level = feature_level['*']
    if not language_level:
      return False
    classifier_level = None
    if fragment['classifier'] in language_level:
      classifier_level = language_level[fragment['classifier']]
    elif '*' in language_level:
      classifier_level = language_level['*']
    if not classifier_level:
      return False
    for pattern in classifier_level:
      if self.pattern_matches(pattern, classifier_level[pattern], fragment['name']):
        return True
    return False


  def aggregate(self, path):
    simplepath = path.replace(self.rooturl, '')
    print "Operating in " + colored(simplepath, 'blue')
    print path
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
        candidates = filter(lambda f: self.is_candidate(f, feature), data['fragments'])
        for c in candidates:
          print " > Checking " + colored(c['name'], 'cyan') + ' (' + colored(c['classifier'] , 'cyan') + ')'
          self.features[feature] = filter(lambda r: r['resource'] not in c['resource'], self.features[feature])
        self.features[feature].extend(candidates)


  def getLocations(self):
    self.aggregate(self.baseresourceurl)

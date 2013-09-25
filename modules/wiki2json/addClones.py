import json
import urllib2
import sys

dumppath = sys.argv[1]
dump = json.load(open(dumppath))
clones = json.load(urllib2.urlopen('http://101companies.org/api/clones'))
for c in clones:
  if not any(map(lambda p: 'p' in p['page'] and p['page']['p'] == "Contribution" and p['page']['n'] == c['title'], dump['wiki']['pages'])):
    if c['status'] == 'created':
      print "Adding " + c['title']
      dump['wiki']['pages'].append({'type' : 'Subject', 'page': {'p': 'Contribution', 'n': c['title']}, 'headline': "...", 'implements': [], 'uses': [], 'instanceOf': [ {'p': 'Namespace', 'n': 'Contribution'}], 'developedBy': []})
with open(dumppath, 'w') as outfile:
  json.dump(dump, outfile)

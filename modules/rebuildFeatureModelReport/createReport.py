import sys
import json
import urllib2
import checker
import tripleLoader

def writeReport(report, pathBase):
  with open(pathBase + '.json', 'w+') as reportf:
    json.dump(report, reportf)
  with open(pathBase + '.jsonp', 'w+') as reportpf:
    reportpf.write('callback(' + json.dumps(report) + ')')

contribNames = sorted(json.loads(file(sys.argv[3]).read())['dirs'])
allSupportedClaferFeatures = sorted(json.loads(file(sys.argv[1]).read()))
summary = {}
# load features and convert to clafer names
rawFeatureTriples = tripleLoader.load("Namespace-3AFeature")
instanceOfURL = 'http://101companies.org/property/instanceOf'
namespaceURL = 'http://101companies.org/resource/Namespace-3ANamespace'
featureTriples = filter(lambda t : t['predicate'] == instanceOfURL and (t['node'] != namespaceURL),  rawFeatureTriples)
allClaferFeatures = map(lambda t : tripleLoader.urlToClafer(t['node'], 'Feature-3A'), featureTriples)
claferTreeRaw = urllib2.urlopen('http://data.101companies.org/dumps/features.clf.json')
claferTree = json.load(claferTreeRaw)['structure']
# check all contributions
for contribName in contribNames:
  print 'Checking ' + contribName + '...',
  report = checker.check(contribName, claferTree, allSupportedClaferFeatures, sys.argv[2])
  print 'done.'
  writeReport(report, sys.argv[4] + sys.argv[5] + contribName)
  summary[contribName] = report
writeReport(summary, sys.argv[4] + 'featureModelReport')

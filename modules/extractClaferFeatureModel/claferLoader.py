import re
import argparse
import tripleLoader
from termcolor import colored
import json

basePropURL = 'http://101companies.org/property/'
baseResURL = 'http://101companies.org/resource/'

leafs = []
cache = []
implications = []

def loadFeature(feat, claferFeat, indent):
  print ' ' * indent + claferFeat,
  if claferFeat in cache:
    print colored('~ DUPLICATE', 'yellow')
    return ['', []]
  cache.append(claferFeat)
  triples = tripleLoader.load(feat)
  isLeaf = all(map(lambda t: t['predicate'] != basePropURL + 'isA' or t['direction'] != 'IN', triples))
  res = '\n' + ' ' * indent
  optional = any(map(lambda t: t['predicate'] == basePropURL + 'isA' and t['direction'] == 'OUT' and t['node'] ==  'Optional feature', triples))
  mandatory = any(map(lambda t: t['predicate'] == basePropURL + 'isA' and t['direction'] == 'OUT' and t['node'] ==  'Mandatory feature', triples))
  alternative = any(map(lambda t: t['predicate'] == basePropURL + 'isA' and t['direction'] == 'OUT' and t['node'] ==  'Alternative feature', triples))
  or_ = any(map(lambda t: t['predicate'] == basePropURL + 'isA' and t['direction'] == 'OUT' and t['node'] ==  'Or feature', triples))
  impliedFeatsTriples = filter(lambda t: t['predicate'] == basePropURL + 'implies' and t['direction'] == 'OUT' ,triples)
  impliedClaferFeats = map(lambda t:  tripleLoader.urlTourlName(tripleLoader.urlNameToClafer(t['node']),'Feature:'), impliedFeatsTriples)
  print colored('=> (' + ', '.join(impliedClaferFeats) + ')', 'cyan'),
  for implied in impliedClaferFeats:
    implications.append([claferFeat, implied])
  if isLeaf:
    leafs.append(claferFeat)
    print colored('~', 'green'),
    res += re.sub("Feature:", "", claferFeat)
    if optional:
      print colored( 'OPTIONAL', 'green'),
      res += ' ?'
    print colored('LEAF', 'green')
    return [res, re.sub("Feature:", "", claferFeat)]
  else:
    if optional:
      print colored('~ OPTIONAL', 'blue'),
      if alternative:
        print colored('ALTERNATIVE (MUX)', 'blue'),
        res += 'mux ' + re.sub("Feature:", "", claferFeat)
      if or_:
        print colored('OR (ANY)', 'blue'),
        res += 'any ' + re.sub("Feature:", "", claferFeat)
    if mandatory:
      print colored('~ MANDATORY', 'blue'),
      if alternative:
        print colored('ALTERNATIVE (XOR)', 'blue'),
        res += 'xor ' + re.sub("Feature:", "", claferFeat)
      if or_:
        print colored('OR (OR)', 'blue'),
        res += 'or ' + re.sub("Feature:", "", claferFeat)
    print colored('NODE', 'blue')
    subFeatTriples = filter(lambda t: t['predicate'] == basePropURL + 'isA' and t['direction'] == 'IN', triples)
    subStr = ""
    subOs = {}
    for ft in subFeatTriples:
      feat = tripleLoader.urlTourlName(ft['node'], 'Feature:')
      claferFeat = tripleLoader.urlNameToClafer(feat)
      [subFeat, o] = loadFeature(feat, claferFeat, indent + 2)
      if len(o) > 0:
        subOs[re.sub("Feature:", "", claferFeat)] = o
      subStr += subFeat
    return [res + subStr, subOs]


def loadRequirement(req, claferReq, indent):
  print claferReq + 's'
  triples = tripleLoader.load(req)
  reqTriples = filter(lambda t: t['node'].find('Feature:') != -1 and t['predicate'] == basePropURL + 'isA' and t['direction'] == 'IN', triples)
  features = ''
  featOs = {}
  for rt in reqTriples:
    feat = tripleLoader.urlTourlName(rt['node'], 'Feature:')
    claferFeat = tripleLoader.urlNameToClafer(feat)
    [f, o] = loadFeature(feat, claferFeat, indent + 2)
    features += f
    if len(o) > 0:
      featOs[re.sub("Feature:", "", claferFeat)] = o
  return ('\n' + ' ' * indent + claferReq + features + '\n', featOs)

#main
parser = argparse.ArgumentParser()
parser.add_argument('-cf', required=True, help='file to write clafer model to')
parser.add_argument('-flatf', required=True, help='file to write flat list of clafer features to')
args = parser.parse_args()
reqsTriples = filter(lambda t: t['predicate'] == basePropURL + 'isA',  tripleLoader.load('Requirement'))
res = 'abstract FeatureSpec'
res += '\n'
reqsObject = {}
for rt in reqsTriples:
  req = tripleLoader.urlTourlName(rt['node'], '')
  claferReq = tripleLoader.urlNameToClafer(req)
  [r, o] = loadRequirement(req, claferReq, 2)
  res += r
  if len(o) > 0:
    reqsObject[claferReq] = o
res += '\n  ' + '\n  '.join(map(lambda t: '[' + re.sub("Feature:", "", t[0]) + ' => ' + re.sub("Feature:", "", t[1]) + ']', implications))
with open(args.cf, 'w+') as f:
  f.write(res)
with open(args.flatf, 'w+') as f:
  f.write(json.dumps(leafs))
with open(args.cf + '.json', 'w+') as f:
  json.dump(reqsObject, f)

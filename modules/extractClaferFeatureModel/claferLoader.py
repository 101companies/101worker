import re
import argparse
import tripleLoader
from termcolor import colored
import json

basePropURL = 'http://101companies.org/property/'
baseResURL = 'http://101companies.org/resource/'

cache = []
implications = []

def loadFeature(featURL, indent):
  feat = tripleLoader.urlTourlName(featURL, 'Feature-3A')
  claferFeat = tripleLoader.urlNameToClafer(feat)
  print ' ' * indent + claferFeat,
  if claferFeat in cache:
    print colored('~ DUPLICATE', 'yellow')
    return ''
  cache.append(claferFeat)
  triples = tripleLoader.load('Feature-3A' + feat)
  isLeaf = all(map(lambda t: t['predicate'] != basePropURL + 'isA' or t['direction'] != 'IN', triples))
  res = '\n' + ' ' * indent
  optional = map(lambda t: t['predicate'] == basePropURL + 'isA' and t['direction'] == 'OUT' and t['node'] == baseResURL + 'Optional_feature', triples)
  impliedFeatsTriples = filter(lambda t: t['predicate'] == basePropURL + 'implies' and t['direction'] == 'OUT' ,triples)
  impliedClaferFeats = map(lambda t:  tripleLoader.urlTourlName(tripleLoader.urlNameToClafer(t['node']),'Feature-3A'), impliedFeatsTriples)
  print colored('=> (' + ', '.join(impliedClaferFeats) + ')', 'cyan'),
  for implied in impliedClaferFeats:
    implications.append([claferFeat, implied])
  if isLeaf:
    print colored('~', 'green'),
    res += claferFeat
    if optional:
      print colored( 'OPTIONAL', 'green'),
      res += ' ?'
    print colored('LEAF', 'green')
    return res
  else:
    print colored('~ NODE', 'blue')
    res += 'mux ' + claferFeat
    subFeatTriples = filter(lambda t: t['predicate'] == basePropURL + 'isA' and t['direction'] == 'IN', triples)
    return res + ''.join(map(lambda t: loadFeature(t['node'], indent + 2), subFeatTriples))


def loadRequirement(reqURL, indent):
  req = tripleLoader.urlTourlName(reqURL, '')
  claferReq = tripleLoader.urlNameToClafer(req)
  print claferReq + 's'
  triples = tripleLoader.load(req)
  reqTriples = filter(lambda t: t['node'].find('Feature-3A') != -1 and t['predicate'] == basePropURL + 'isA' and t['direction'] == 'IN', triples)
  features = ''.join(map(lambda t:  loadFeature(t['node'], indent + 2), reqTriples))
  return '\n' + ' ' * indent + claferReq + features + '\n'

#main
parser = argparse.ArgumentParser()
parser.add_argument('-cf', required=True, help='file to write clafer model to')
parser.add_argument('-flatf', required=True, help='file to write flat list of clafer features to')
args = parser.parse_args()
reqsTriples = filter(lambda t: t['predicate'] == basePropURL + 'isA',  tripleLoader.load('Requirement'))
res = 'abstract FeatureSpec'
res += '\n' + ''.join(map(lambda t: loadRequirement(t['node'],2), reqsTriples))
res += '\n  ' + '\n  '.join(map(lambda t: '[' + t[0] + ' => ' + t[1] + ']', implications))
with open(args.cf, 'w+') as f:
  f.write(res)
with open(args.flatf, 'w+') as f:
  f.write(json.dumps(cache))

import sys
import tripleLoader

def printIndent(o, indent, implemented):
  res = ''
  for k in o.keys():
   res += ' ' * indent
   if k not in implemented and isinstance(o[k], basestring):
    res += 'no '
   res += k + '\n'
   if not isinstance(o[k], basestring):
    res += printIndent(o[k], indent + 1, implemented)
  return res

def contribToClafer(contrib, claferTree, allFeatures):
  triples = tripleLoader.load( "Contribution-3A" + contrib)
  implementedTriples = filter(lambda t : t['predicate'] == "http://101companies.org/property/implements", triples)
  implemented = map(lambda t : tripleLoader.urlToClafer(t['node'], 'Feature-3A'), implementedTriples)
  print implemented
  notImplemented = set(allFeatures) - set(implemented)
  print printIndent(claferTree, 0, implemented)
  if not implemented:
    raise Exception("No implemented features specified.")
  return contrib.title() + " : FeatureSpec\n [ \n" + printIndent(claferTree, 0, implemented) + '\n]'


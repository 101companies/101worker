import sys
import tripleLoader

def contribToClafer(contrib, allFeatures):
  triples = tripleLoader.load( "Contribution-3A" + contrib)
  implementedTriples = filter(lambda t : t['predicate'] == "http://101companies.org/property/implements", triples)
  implemented = map(lambda t : tripleLoader.urlToClafer(t['node'], 'Feature-3A'), implementedTriples)
  notImplemented = set(allFeatures) - set(implemented)
  if not implemented:
    raise Exception("No implemented features specified.")
  output = contrib.title() + " : FeatureSpec\n [ "
  output += '\n   '.join(cf for cf in implemented)
  output += '\n   ' + '\n   '.join('no ' + cf for cf in notImplemented)
  output +=  "]"
  return output


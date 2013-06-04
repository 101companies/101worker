from tools import loadPage
from tools import dot
import json

def _extractFeatures(url):
    triples = loadPage(url)
    features = []

    for triple in triples:
        predicate = triple[1]
        object = triple[2]

        if predicate == 'http://101companies.org/property/implements':
            features.append(object.replace('http:/101companies.org/resources/features/', ''))
    return features

def deriveFeaturesForContributions(blacklist = []):
    contributions = loadPage('http://localhost/services/discovery/contributions')['members']
    featuresContributions = {}
    missingFeatures = []

    for contribution in contributions:
        if contribution['name'] in blacklist:
            continue

        data = loadPage(contribution['resource'])
        features = _extractFeatures(data['endpoint'])

        if not features:
            missingFeatures.append(contribution['resource'])
        else:
            key = tuple(features)
            if not key in featuresContributions:
                featuresContributions[key] = {'features': features, 'contributions': []}
            featuresContributions[key]['contributions'].append(contribution['name'])

        dot()


    lst = sorted(featuresContributions.values(), key=lambda k: len(k['contributions']))

    json.dump(lst, open('debugOutput/features.json', 'w'), indent=4)
    json.dump(missingFeatures, open('debugOutput/missingFeatures.json', 'w'), indent=4)

    return lst
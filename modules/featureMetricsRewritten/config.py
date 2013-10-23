import warnings
from metamodel import *

featuresToInspect = set(['total', 'cut', 'hierarchical company'])

#include company and employee to java hierarchical company feature
#check javastatic and javacomposition if they also implement depth
contributionWhitelist = [
    Member('contributions/haskellSyb'), Member('contributions/haskellComposition'), Member('contributions/jdom'),
    Member('contributions/javaStatic'), Member('contributions/javaComposition'), Member('contributions/javaInheritance'),
    Member('contributions/pyjson')
]

implicitlyImplemented = {
    'jdom'  : ['hierarchical company'],
    'pyjson': ['hierarchical company']
}

def validateAutomaticTagging(featureIndex):
    for feature in featuresToInspect:
        for file in featureIndex.get(feature, []):
            if file.member in contributionWhitelist and file.relevance == 'system':
                metadataUnits = file.matches.filter(lambda x: 'feature' in x and x['feature'] == feature)
                if len(metadataUnits) < 2:
                    warnings.warn('{} has odd number of metadata units'.format(file.identifier))
                    if metadataUnits[0].get('manual', False):
                        warnings.warn('Automatic tagging missed {} for feature {}'.format(file.identifier, feature))
                    else:
                        warnings.warn(
                            '{} is either missing automatic tagging or validation of feature {}'.format(file.identifier,
                                                                                                       feature))
                else:
                    if (not metadataUnits[0].get('manual', False) and metadataUnits[1].get('manual', False)) or (
                            metadataUnits[0].get('manual', False) and not metadataUnits[1].get('manual', False)):
                        #everythings fine
                        pass
                    else:
                        warnings.warn(
                            '{} is either missing automatic tagging or validation of feature {}'.format(file.identifier,
                                                                                                        feature))
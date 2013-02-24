#! /usr/bin/env python

import sys
import json
import re

sys.path.append('../../libraries/101meta')
import const101
import tools101


# loading of the dumps this module depends on
repo = json.load(open(const101.pullRepoDump, 'r'))
rules = json.load(open(const101.rulesDump, 'r'))["results"]["rules"]
wiki = json.load(open(const101.wikiDump, 'r'))["wiki"]
wikiUrl = 'http://101companies.org/wiki/{0}'

### HELPER FUNCTIONS
def encodeForUrl(str):
    return str.replace(' ', '_')


def findWikiEntry(val, pageName, map):
    """
    check if the wiki has an entry with pagename, create a entry in map with the values and add it to the problems list if
    there is any trouble (not found in the wiki)
    :param val: they key under which the entry will be created in map
    :param pageName: the page name, wich will be checked and appended to the wiki url
    :param map: the map into which the results will be saved
    """
    for page in wiki['pages']:
        if page['page']['page'] == pageName.replace('_', ' '):
            map[val] = {
                '101wiki': wikiUrl.format(encodeForUrl(pageName)),
                'headline': '<not implemented>'
            }
            return

    map[val] = {'101wiki': '<unresolved>', 'headline': '<not implemented>'}
    problems.append({'missingWikiPage': wikiUrl.format(encodeForUrl(pageName))})


def handleMention(unit, key, map, pageNameFunc):
    """
    checks if the unit contains the key - if yes, it will add a wiki entry to map if necessary
    :param unit: the metadata entry that has to be inspected
    :param key: the key to look for (e.g. language)
    :param map: the map the results will be added to
    :param pageNameFunc: a function that's mapping the value found under the key to it's supposed page name in the wiki
    """
    if key in unit:
        val = unit[key]
        if not val in map:
            findWikiEntry(val, pageNameFunc(val), map)

def handleContribution(name, map):
    """
    Looks up the repo url for the contribution and adds an entry to map for it. If the URL can't be found, it will also
    create an entry in the problems list
    :param name: name of the contribution
    :param map: map in which the entry is created
    """
    repoUrl = '<unresolved>'
    if name in repo:
        repoUrl = repo[name]
    else:
        problems.append({'missing repo url' : name})

    map[name] = {
        '101wiki' : wikiUrl.format(page['page']['page']),
        '101repo' : repoUrl,
        'headline': 'not implemented'
    }


### MAIN PROGRAM
# variables that will form the dump later on
terms = dict()
concepts = dict()
features = dict()
languages = dict()
technologies = dict()
contributions = dict()
results = dict()
results["terms"] = terms
results["concepts"] = concepts
results["features"] = features
results["languages"] = languages
results["technologies"] = technologies
results["languages"] = languages
results["contributions"] = contributions
problems = list()

# First part - check metadata values - they are supposed to have a page in the wiki
for rule in rules:
    for unit in rule['rule']['metadata']:
        handleMention(unit, "concept", concepts, lambda x: x)
        handleMention(unit, "language", languages, lambda x: 'Language:' + x)
        handleMention(unit, "dependsOn", technologies, lambda x: 'Technology:' + x)
        handleMention(unit, "inputOf", technologies, lambda x: 'Technology:' + x)
        handleMention(unit, "outputOf", technologies, lambda x: 'Technology:' + x)
        handleMention(unit, "partOf", technologies, lambda x: 'Technology:' + x)
        handleMention(unit, "term", terms, lambda x: '101term:' + x)
        handleMention(unit, "feature", features, lambda x: 'Feature:' + x)

# Second part - check that contributions in the wiki actually exist (have a repository link)
regex = re.compile('Contribution:(?P<name>.+)')
for page in wiki['pages']:
    match = regex.match(page['page']['page'])
    if match:
        handleContribution(match.group('name'), contributions)

# creation of the dump
dump = dict()
dump["results"] = results
dump["numbers"] = dict()
dump["numbers"]["numbersOfTerms"] = len(terms)
dump["numbers"]["numbersOfConcepts"] = len(concepts)
dump["numbers"]["numbersOfFeatures"] = len(features)
dump["numbers"]["numbersOfLanguages"] = len(languages)
dump["numbers"]["numbersOfTechnologies"] = len(technologies)
dump["numbers"]["numbersOfContributions"] = len(contributions)
dump["problems"] = problems
tools101.releaseDump(dump, const101.resolutionDump)
#! /usr/bin/env python

import sys
import json
import re

sys.path.append('../../libraries/101meta')
import const101
import tools101
import urllib2


# loading of the dumps this module depends on
repo = json.load(open(const101.pullRepoDump, 'r'))
rules = json.load(open(const101.rulesDump, 'r'))["results"]["rules"]
wiki = json.load(open(const101.wikiDump, 'r'))["wiki"]
wikiUrl = 'http://101companies.org/wiki/{0}'

### HELPER FUNCTIONS
def encodeForUrl(ns, name):
    if not ns: return name.replace(' ', '_')
    return (ns + ':' + name).replace(' ', '_')

def getHeadline(pageName):
    print 'Looking for wiki data of {0}'.format(pageName)
    url = 'http://beta.101companies.org/api/pages/{0}/sections'.format(pageName)
    try:
        a = urllib2.urlopen(url)
    except urllib2.HTTPError as e:
        if e.code == 500:
            print 'There was an error: {0} - trying again...'.format(e)
            return getHeadline(pageName)

    pageData = json.load(a)
    for d in pageData:
        if d['title'] == 'Headline':
            return d['content'].replace('== Headline ==\n\n', '').replace('[[', '').replace(']]', '').replace('\n', '')

def findWikiEntry(val, namespace, title, map):
    """
    check if the wiki has an entry with namespace:title, create a entry in map with the values and add it to the problems list if
    there is any trouble (not found in the wiki)
    :param val: they key under which the entry will be created in map
    :param namespace the namespace in which to look
    :param title the title of the wiki entry
    :param map: the map into which the results will be saved
    """
    for page in wiki['pages']:
        if page['page']['page']['ns'] == namespace and page['page']['page']['title'] == title.replace('_', ' '):
            map[val] = {
                '101wiki': wikiUrl.format(encodeForUrl(namespace,title)),
                'headline': getHeadline(encodeForUrl(namespace,title))
            }
            return

    map[val] = {'101wiki': '<unresolved>', 'headline': '<unresolved>'}
    problems.append({'missingWikiPage': wikiUrl.format(encodeForUrl(namespace, title))})


def handleMention(unit, key, map, namespace):
    """
    checks if the unit contains the key - if yes, it will add a wiki entry to map if necessary
    :param unit: the metadata entry that has to be inspected
    :param key: the key to look for (e.g. language)
    :param map: the map the results will be added to
    :param namespace: the namespace in which to search
    """
    if key in unit:
        val = unit[key]
        if not val in map:
            findWikiEntry(val, namespace, val, map)

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
    pageName = page['page']['page']['ns'] + ':' + page['page']['page']['title']
    map[name] = {
        '101wiki' : wikiUrl.format(pageName),
        '101repo' : repoUrl,
        'headline': getHeadline(pageName)
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
results["contributions"] = contributions
problems = list()

# First part - check metadata values - they are supposed to have a page in the wiki
for rule in rules:
    for unit in rule['rule']['metadata']:
        handleMention(unit, "concept", concepts, None)
        handleMention(unit, "language", languages,    'Language')
        handleMention(unit, "dependsOn", technologies,'Technology')
        handleMention(unit, "inputOf", technologies,  'Technology')
        handleMention(unit, "outputOf", technologies, 'Technology')
        handleMention(unit, "partOf", technologies,   'Technology')
        handleMention(unit, "term", terms,            '101term')
        handleMention(unit, "feature", features, None)


# Second part - check that contributions in the wiki actually exist (have a repository link)
#regex = re.compile('Contribution:(?P<name>.+)')
for page in wiki['pages']:
    if page['page']['page']['ns'] == 'Contribution':
        handleContribution(page['page']['page']['title'], contributions)

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
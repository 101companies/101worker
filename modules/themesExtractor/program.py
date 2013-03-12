#!/usr/bin/python
import json
import sys
import os
import urllib2

json_path = sys.argv[1]

wiki = json.load(open(json_path, 'r'))['wiki']
pages = wiki['pages']
themes = filter(lambda p: "Theme" == p['page'].get('page', {}).get('p', ''), pages)

def getRealFeature(f, pages):
    f = f.replace('_', ' ')
    def filter_func(p):
        return p['page']['page']['p'] == 'Feature' and p['page']['page']['n'] == f

    try:
        return filter(filter_func, pages)[0]
    except IndexError:
        return {
            'page': {
                'headline': ''
            }
        }

def getRealConcept(f, pages):
    f = f.replace('_', ' ')
    def filter_func(p):
        return p['page']['page']['p'] is None and p['page']['page']['n'] == f

    try:
        return filter(filter_func, pages)[0]
    except IndexError:
        return {
            'page': {
                'headline': ''
            }
        }

def getRealTechnology(f, pages):
    f = f.replace('_', ' ')
    def filter_func(p):
        return p['page']['page']['p'] == 'Technology' and p['page']['page']['n'] == f

    try:
        return filter(filter_func, pages)[0]
    except IndexError:
        return {
            'page': {
                'headline': ''
            }
        }

def getContributionNames(pages):
    return map(lambda p: p['page']['page']['n'], pages)

def getThemeName(theme):
    return theme.replace(' ', '_')

def getThemeNames(themes):
    for p in themes:
        t = p['page']
        yield t['page']['n']

def getAttr(pages, attr):
    s = []
    for p in pages:
        p = p['page']
        s += p.get(attr, [])
    return s

def names(ps):
    return map(lambda p: p['n'], ps)

def getUnique(page, pages, attr):
    f = getAttr(page, attr)
    features =  getAttr(pages, attr)
    unique = filter(lambda p: features.count(p) == 1, f)
    return unique

def getLangs(pages):
    pages = getAttr(pages, 'uses')
    return map(lambda i: i['n'], filter(lambda i: i['p'] == 'Language', pages))

def getUniqueLanguages(page, pages):
    langs = getLangs(pages)
    l = getLangs(page)
    unique = filter(lambda p: langs.count(p) == 1, l)
    return unique
    
def getTechs(pages):
    pages = getAttr(pages, 'uses')
    return map(lambda i: i['n'], filter(lambda i: i['p'] == 'Technology', pages))

def getUniqueTechs(page, pages):
    techs = getTechs(pages)
    t = getTechs(page)
    unique = filter(lambda p: techs.count(p) == 1, t)
    return unique

def getConcepts(pages):
    pages = getAttr(pages, 'instanceOf')
    return map(lambda i: i['n'], filter(lambda i: i['p'] is None, pages))

def getUniqueConcepts(page, pages):
    concepts = getConcepts(pages)
    c = getConcepts(page)
    unique = filter(lambda p: concepts.count(p) == 1, page)
    return concepts

def getThemeInstances(theme, pages):
    instance_theme_name = getThemeName(theme)
    def filter_func(p):
        ins = p['page'].get('instanceOf', [])
        for i in ins:
            if i['p'] == 'Theme' and i['n'] == instance_theme_name:
                return True

        return False
    
    return filter(filter_func, pages)

def createMembers(theme, pages):
    instances = getThemeInstances(theme, pages)
        
    for instance in instances:
        name = instance['page'].get('page', {}).get('n', '')

        unique_f = map(lambda i: i['n'], getUnique([instance], instances, 'implements'))
        num_f = len(set(map(lambda i: i['n'], getAttr([instance], 'implements'))))
        
        unique_l = getUniqueLanguages([instance], instances)
        num_l = len(set(getLangs([instance])))
        
        unique_t = getUniqueTechs([instance], instances)
        num_t = len(set(getTechs([instance])))

        unique_c = getUniqueConcepts([instance], instances)
        num_c = len(set(getConcepts([instance])))
        
        headline = instance['page'].get('headline', '')
        
        yield {
        
            'name': name,
            'headline': headline,
            'features': num_f,
            'ufeatures': unique_f,
            
            'languages': num_l,
            'ulanguages': unique_l,
            
            'technologies': num_t,
            'utechnologies': unique_t,

            'concepts': num_c,
            'uconcepts': unique_c
        
        }

def getContributionsWithFeature(feature, pages):
    def filter_func(p):
        implements = p['page'].get('implements', [])
        for i in implements:
            if i['p'] == 'Feature' and i['n'] == feature:
                return True

    f = filter(filter_func, pages)
    return f

def getContributionsWithConcept(name, pages):
    def filter_func(p):
        implements = p['page'].get('instanceOf', [])
        for i in implements:
            if i['p'] is None and i['n'] == name:
                return True

    f = filter(filter_func, pages)
    return f

def getContributionsWithTechnology(name, pages):
    def filter_func(p):
        implements = p['page'].get('uses', [])
        for i in implements:
            if i['p'] == 'Technology' and i['n'] == name:
                return True

    f = filter(filter_func, pages)
    return f
        
def createFeatures(theme, pages):
    theme_pages = getThemeInstances(theme, pages)
    features = getAttr(theme_pages, 'implements')
    feature_names = names(features)
    
    for feature in feature_names:
        rf = getRealFeature(feature, pages)
        contributions = getContributionsWithFeature(feature, theme_pages)
        headline = rf['page'].get('headline', '')
        contributions = getContributionNames(contributions)
        resolved = bool(rf['page'].get('resolved', ''))
        
        yield {
            'name': feature,
            'headline': headline,
            'contributions': contributions,
            'resolved': resolved
        
        }

def createConcepts(theme, pages):
    theme_pages = getThemeInstances(theme, pages)
    concepts = getConcepts(theme_pages)
    
    for concept in concepts:
        rf = getRealConcept(concept, pages)
        contributions = getContributionsWithConcept(concept, theme_pages)
        headline = rf['page'].get('headline', '')
        contributions = getContributionNames(contributions)
        resolved = bool(rf['page'].get('resolved', ''))
        
        yield {
            'name': concept,
            'headline': headline,
            'contributions': contributions,
            'resolved': resolved
        
        }

def createTechnologies(theme, pages):
    theme_pages = getThemeInstances(theme, pages)
    technologies = getTechs(theme_pages)
    
    for tech in technologies:
        rf = getRealTechnology(tech, pages)
        contributions = getContributionsWithTechnology(tech, theme_pages)
        headline = rf['page'].get('headline', '')
        contributions = getContributionNames(contributions)
        resolved = bool(rf['page'].get('resolved', ''))
        
        yield {
            'name': tech,
            'headline': headline,
            'contributions': contributions,
            'resolved': resolved
        
        }

for t in getThemeNames(themes):
    
    members = list(createMembers(t, pages))

    if not members:
        continue

    if not os.path.exists('output'):
        os.mkdir('output')
    if not os.path.exists(os.path.join('output', t)):
        os.mkdir(os.path.join('output', t))
    path = os.path.join('output', t, 'members.json')
    
    f = open(path, 'w')
    f.write(json.dumps(members, indent=4, sort_keys=True))
    f.close()   
    
    path = os.path.join('output', t, 'features.json')
    f = open(path, 'w')
    features = list(createFeatures(t, pages))
    f.write(json.dumps(features, indent=4, sort_keys=True))
    f.close()

    path = os.path.join('output', t, 'concepts.json')
    f = open(path, 'w')
    features = list(createConcepts(t, pages))
    f.write(json.dumps(features, indent=4, sort_keys=True))
    f.close()  

    path = os.path.join('output', t, 'technologies.json')
    f = open(path, 'w')
    features = list(createTechnologies(t, pages))
    f.write(json.dumps(features, indent=4, sort_keys=True))
    f.close()  
        

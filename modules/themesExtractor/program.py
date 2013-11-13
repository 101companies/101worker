#!/usr/bin/python
import json
import sys
import os
import urllib2
import asq
from asq.initiators import query
import re
from jinja2 import FileSystemLoader, Environment, evalcontextfilter
import shutil

sys.path.append('../../libraries/101meta')
sys.path.append('../../libraries')
import const101
import tools101
from mediawiki import remove_headline_markup

output = os.path.join(const101.tRoot, 'themes')
output = os.path.abspath(output)

json_path = sys.argv[1]

wiki = json.load(open(json_path, 'r'))['wiki']
pages = wiki['pages']
themes = filter(lambda p: "Theme" == p.get('p', ''), pages)

for d in os.listdir(output):
    if os.path.isdir(os.path.join(output, d)):
        shutil.rmtree(os.path.join(output, d))

def render(d):
    if isinstance(d, list):
        return ', '.join(d)
    else:
        return d

def getRealFeature(f, pages):
    f = f.replace('_', ' ')
    def filter_func(p):
        return p['p'] == 'Feature' and p['n'].lower() == f.lower()

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
        return p['page']['p'] is None and p['page']['n'].lower() == f.lower()

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
        return p['page']['p'] == 'Technology' and p['page']['n'].lower() == f.lower()

    try:
        return filter(filter_func, pages)[0]
    except IndexError:
        return {
            'page': {
                'headline': ''
            }
        }

def getContributionNames(pages):
    return map(lambda p: p['n'], pages)

def getThemeName(theme):
    return theme.replace(' ', '_')

def getThemeNames(themes):
    for p in themes:
        yield p['n']

def getAttr(pages, attr):
    s = []
    for p in pages:
        s += p.get(attr, [])
    return s

def names(ps):
    return map(lambda p: p['n'], ps)

def getLangs(pages):
    langs = query(pages).where(lambda p: any(filter(lambda i: i.startswith('uses::Language'), p.get('internal_links', [])))) \
        .select(lambda p: filter(lambda i: i.startswith('uses::Language'), p['internal_links'])).to_list()
    s = reduce(lambda a, b: a + b, langs) if langs else []
    return map(lambda n: n.replace('uses::Language:', ''), s)

def getUniqueLanguages(page, pages):
    langs = getLangs(pages)
    l = getLangs(page)
    unique = filter(lambda p: langs.count(p) == 1, l)
    return unique
    
def getTechs(pages):
    techs = query(pages).where(lambda p: any(filter(lambda i: i.startswith('uses::Technology'), p.get('internal_links', [])))) \
        .select(lambda p: filter(lambda i: i.startswith('uses::Technology'), p['internal_links'])).to_list()
    s = reduce(lambda a, b: a + b, techs) if techs else []
    return map(lambda n: n.replace('uses::Technology:', ''), s)

def getUniqueTechs(page, pages):
    techs = getTechs(pages)
    t = getTechs(page)
    unique = filter(lambda p: techs.count(p) == 1, t)
    return unique

def getConcepts(pages):
    cs = query(pages).where(lambda p: any(filter(lambda i: re.match(r'^[a-zA-Z0-9 ]+$', i), p.get('internal_links', [])))) \
        .select(lambda p: filter(lambda i: re.match(r'^[a-zA-Z0-9 ]+$', i), p['internal_links'])).to_list()
    s = reduce(lambda a, b: a + b, cs) if cs else []
    return s


def getFeatures(pages):
    techs = query(pages).where(lambda p: any(filter(lambda i: i.startswith('implements::Feature:'), p['page'].get('internal_links', [])))) \
        .select(lambda p: filter(lambda i: i.startswith('implements::Feature:'), p['page']['internal_links'])).to_list()
    s = reduce(lambda a, b: a + b, techs) if techs else []
    return map(lambda n: n.replace('implements::Feature:', ''), s)

def getUniqueConcepts(page, pages):
    concepts = getConcepts(pages)
    c = getConcepts(page)
    unique = filter(lambda p: concepts.count(p) == 1, c)
    return unique

def getUniqueFeatures(page, pages):
    features = getFeatures(pages)
    c = getFeatures(page)
    unique = filter(lambda p: features.count(p) == 1, c)
    return unique


def getThemeInstances(theme, pages):
    print 'instanceOf::Theme:' + theme
    insts = query(pages).where(lambda p: any(filter(lambda i: i == 'instanceOf::Theme:' + theme, p['internal_links']))).to_list()
    print insts
    return insts

def createMembers(theme, pages):
    instances = getThemeInstances(theme, pages)
        
    for instance in instances:
        name = instance['page'].get('n', '')

        unique_f = getUniqueFeatures([instance], instances)
        num_f = getFeatures([instance])
        
        unique_l = getUniqueLanguages([instance], instances)
        num_l = list(set(getLangs([instance])))
        
        unique_t = getUniqueTechs([instance], instances)
        num_t = list(set(getTechs([instance])))

        unique_c = getUniqueConcepts([instance], instances)
        num_c = list(set(getConcepts([instance])))
        
        headline = remove_headline_markup(instance['page'].get('headline', ''))
        
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
        f = getFeatures([p])
        return feature in f

    f = filter(filter_func, pages)
    return f

def getContributionsWithConcept(name, pages):
    def filter_func(p):
        f = getConcepts([p])
        return name in f
        #implements = p['page'].get('instanceOf', [])
        #for i in implements:
        #    if i['p'] is None and i['n'] == name:
        #        return True

    f = filter(filter_func, pages)
    return f

def getContributionsWithTechnology(name, pages):
    def filter_func(p):
        t = getTechs([p])
        return name in t
        #implements = p['page'].get('uses', [])
        #for i in implements:
        #    if i['p'] == 'Technology' and i['n'] == name:
        #        return True

    f = filter(filter_func, pages)
    return f
        
def createFeatures(theme, pages):
    theme_pages = getThemeInstances(theme, pages)
    
    features = list(set(getFeatures(theme_pages)))
    feature_names = features
    
    for feature in feature_names:
        rf = getRealFeature(feature, pages)
        contributions = getContributionsWithFeature(feature, theme_pages)
        headline = remove_headline_markup(rf['page'].get('headline', ''))
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
    concepts = list(set(getConcepts(theme_pages)))
    
    for concept in concepts:
        rf = getRealConcept(concept, pages)
        contributions = getContributionsWithConcept(concept, theme_pages)
        headline = remove_headline_markup(rf['page'].get('headline', ''))
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
    technologies = list(set(getTechs(theme_pages)))
    
    for tech in technologies:
        rf = getRealTechnology(tech, pages)
        contributions = getContributionsWithTechnology(tech, theme_pages)
        headline = remove_headline_markup(rf['page'].get('headline', ''))
        contributions = getContributionNames(contributions)
        resolved = bool(rf['page'].get('resolved', ''))
        
        yield {
            'name': tech,
            'headline': headline,
            'contributions': contributions,
            'resolved': resolved
        }

def deleteEmptyCells(data):
    if not data:
        return data

    cells = data[0].keys()
    for cell in cells:
        if all(not d[cell] for d in data):
            for d in data:
                del d[cell]
    return data

def toTex(list, file):
    with open (file, 'w') as f:
        f.write(',\n'.join(map(lambda x: "\wikipage{" + x['name'] + "}",  list)))

for t in getThemeNames(themes):
    
    members = sorted(list(createMembers(t, pages)), key=lambda s: s['name'])

    if not members:
        continue

    if not os.path.exists(output):
        os.mkdir(output)
    if not os.path.exists(os.path.join(output, t)):
        os.mkdir(os.path.join(output, t))
    path = os.path.join(output, t, 'members.json')
    
    f = open(path, 'w')
    f.write(json.dumps(members, indent=4, sort_keys=True))
    f.close()

    # template stuff
    loader = FileSystemLoader('.')
    env = Environment(loader=loader)
    env.filters['render'] = render
    template = env.get_template('html.tpl')

    f = open(os.path.join(output, t, 'members.html'), 'w')
    f.write(template.render({'data': deleteEmptyCells(members)}))
    f.close()

    template = env.get_template('tex.tpl')

    f = open(os.path.join(output, t, 'members.tex'), 'w')
    f.write(template.render({'data': deleteEmptyCells(members)}))
    f.close()

    toTex(deleteEmptyCells(members), os.path.join(output, t, 'members_list.tex'))
    
    # to here
    
    path = os.path.join(output, t, 'features.json')
    f = open(path, 'w')
    features = sorted(list(createFeatures(t, pages)), key=lambda s: len(s['contributions']))[::-1]
    f.write(json.dumps(features, indent=4, sort_keys=True))
    f.close()

    template = env.get_template('features.html')

    f = open(os.path.join(output, t, 'features.html'), 'w')
    f.write(template.render({'data': deleteEmptyCells(features), 'title': 'Concepts'}))
    f.close()

    template = env.get_template('features.tex')

    f = open(os.path.join(output, t, 'features.tex'), 'w')
    f.write(template.render({'data': deleteEmptyCells(features), 'title': 'Concepts'}))
    f.close()

    toTex(deleteEmptyCells(features), os.path.join(output, t, 'features_list.tex'))

    path = os.path.join(output, t, 'concepts.json')
    f = open(path, 'w')
    concepts = sorted(list(createConcepts(t, pages)), key=lambda s: s['name'])
    f.write(json.dumps(concepts, indent=4, sort_keys=True))
    f.close()  

    template = env.get_template('features.html')

    f = open(os.path.join(output, t, 'concepts.html'), 'w')
    f.write(template.render({'data': deleteEmptyCells(concepts), 'title': 'Concepts'}))
    f.close()

    template = env.get_template('features.tex')

    f = open(os.path.join(output, t, 'concepts.tex'), 'w')
    f.write(template.render({'data': deleteEmptyCells(concepts), 'title': 'Concepts'}))
    f.close()

    toTex(deleteEmptyCells(concepts), os.path.join(output, t, 'concepts_list.tex'))

    path = os.path.join(output, t, 'technologies.json')
    f = open(path, 'w')
    technologies = sorted(list(createTechnologies(t, pages)), key=lambda s: s['name'])
    f.write(json.dumps(features, indent=4, sort_keys=True))
    f.close()  

    template = env.get_template('features.html')

    f = open(os.path.join(output, t, 'technologies.html'), 'w')
    f.write(template.render({'data': deleteEmptyCells(technologies)}))
    f.close()

    template = env.get_template('features.tex')

    f = open(os.path.join(output, t, 'technologies.tex'), 'w')
    f.write(template.render({'data': deleteEmptyCells(technologies)}))
    f.close()

    toTex(deleteEmptyCells(technologies), os.path.join(output, t, 'technologies_list.tex'))
        

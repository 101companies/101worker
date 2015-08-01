#! /usr/bin/env python

import json
import sys
from collections import Counter
from jinja2 import *
import re
import os

# Load 101wiki into memory

# wiki = json.load(open(sys.argv[1], 'r'))['wiki']

# Write .json and .html file -- the latter as a tag cloud
def writeFiles(counts, label, prefix):

    # Write frequency map to JSON
    jsonFile = open(label + '.json', 'w')
    jsonFile.write(json.dumps(counts, indent=4))

    # Prepare for buckets of scaling
    # Inspired by http://stackoverflow.com/questions/3180779/html-tag-cloud-in-python
    step = (max(counts.values()) / 6) or 1

    counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

    loader = FileSystemLoader(os.path.abspath(os.path.join(os.path.dirname(__file__))))
    env = Environment(loader=loader)
    template = env.get_template('tagcloud.html')
    open(label + '.html', 'w').write(template.render({
        'title': label,
        'counts': counts,
        'step': step,
        'root': 'http://101companies.org/wiki/' + prefix
    }))

    ## Apply scaling and write HTML
    #htmlFile = open(label + '.html', 'w')
    #htmlFile.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">\n')
    #htmlFile.write('<html>\n')
    #htmlFile.write('<head>\n')
    #htmlFile.write('  <title>' + label + '</title>\n')
    #htmlFile.write('  <link rel="stylesheet" type="text/css" href="wiki2tagclouds.css"/>\n')
    #htmlFile.write('</head>\n')
    #htmlFile.write('<body>\n')

    #print counts


    #for tag, count in counts:
    #    css = count / step
    #    htmlFile.write('<a href="%s:%s" class="size-%s">%s</a>\n' % (root, tag, css, tag),)

    #htmlFile.write('</body>\n')
    #htmlFile.write('</html>\n')
    #htmlFile.close()

# pages = wiki['pages']
#
# contributions = filter(lambda p: "Contribution" == p.get('p', ''), pages)
# #contributions = [p for p in contributions ]
#
# uses = [p.get('uses', []) for p in contributions]
# uses = [p for use in uses for p in use]
#
# uses = filter(lambda u: u['p'] == 'Language', uses)
#
# uses = [use['n'] for use in uses]
#
# lcounts = Counter(uses)
#
# uses = [p.get('uses', []) for p in contributions]
# uses = [p for use in uses for p in use]
#
# uses = filter(lambda u: u['p'] == 'Technology', uses)
#
# uses = [use['n'] for use in uses]
#
# tcounts = dict(Counter(uses))
#
# writeFiles(lcounts, 'frequencyOfLanguages', 'Language')
# writeFiles(tcounts, 'frequencyOfTechnologies', 'Technology')

import atomos.atom as atom

state = atom.Atom({ 'languages': {}, 'technologies': {} })

def write_html(k, ref, old, new):
    writeFiles(new['languages'], 'frequencyOfLanguages', 'Language')
    writeFiles(new['technologies'], 'frequencyOfTechnologies', 'Technology')

state.add_watch('write_html', write_html)

def add_counts(cur_state, langs, technologies):
    for lang in langs:
        if cur_state['languages'].has_key(lang):
            cur_state['languages'][lang] += 1
        else:
            cur_state['languages'][lang] = 1

    for technology in technologies:
        if cur_state['technologies'].has_key(technology):
            cur_state['technologies'][technology] += 1
        else:
            cur_state['technologies'][technology] = 1

    return cur_state

def main(page):
    page = page['data']

    if page['namespace'] == 'Contribution':
        langs = re.findall(r'uses\:\:language\:([a-zA-Z_ ]+)', page['raw_content'].lower())
        technologies = re.findall(r'uses\:\:technology\:([a-zA-Z_ ]+)', page['raw_content'].lower())

        state.swap(add_counts, langs, technologies)

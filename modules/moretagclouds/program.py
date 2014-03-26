#! /usr/bin/env python

import json
import sys
from collections import Counter
from jinja2 import *

# Load 101wiki into memory

wiki = json.loads(open(sys.argv[1], 'r').read())['wiki']
#wiki = json.loads(open('wiki.json', 'r').read())['wiki']


# Write .json and .html file -- the latter as a tag cloud
def writeFiles(counts, label, prefix):

    # Write frequency map to JSON
    jsonFile = open(label + '.json', 'w')
    jsonFile.write(json.dumps(counts, indent=4))

    # Prepare for buckets of scaling
    # Inspired by http://stackoverflow.com/questions/3180779/html-tag-cloud-in-python
    #step = max(counts.values()) / 6

    #counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    
    #loader = FileSystemLoader('.')
    #env = Environment(loader=loader)
    #template = env.get_template('tagcloud.json')
    #open(label + '.json', 'w').write(template.render({
    #    'title': label,
    #    'counts': counts,
    #    'step': step,
    #    'root': 'http://101companies.org/wiki/' + prefix
    #}))
    
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

pages = wiki['pages']

contributions = filter(lambda p: "Contribution" == p.get('p', ''), pages)
#contributions = [p['page'] for p in contributions ]

uses = [p.get('uses', []) for p in contributions]
uses = [p for use in uses for p in use]

uses = filter(lambda u: u['p'] == 'Language', uses)

uses = [use['n'].replace('_', ' ') for use in uses]

lcounts = Counter(uses)

uses = [p.get('uses', []) for p in contributions]
uses = [p for use in uses for p in use]

uses = filter(lambda u: u['p'] == 'Technology', uses)

uses = [use['n'].replace('_', ' ') for use in uses]

tcounts = dict(Counter(uses))

# features

implements = map(lambda c: c.get('implements', []), contributions)
implements = reduce(lambda a, b: a+b, implements)

features = filter(lambda o: o['p'] == 'Feature', implements)
features = map(lambda o: o['n'], features)

features = [f.replace('_', ' ') for f in features]

fcounts = dict(Counter(features))

#contributors

developedBy = map(lambda c: c.get('developedBy', []), contributions)
developedBy = reduce(lambda a, b: a+b, developedBy)

developedBy = filter(lambda o: o['p'] == 'Contributor', developedBy)
developedBy = map(lambda o: o['n'], developedBy)

developedBy = [d.replace('_', ' ') for d in developedBy]
#developedBy = [ d.decode('utf8') for d in developedBy]

ccounts = dict(Counter(developedBy))

writeFiles(lcounts, 'languages', 'Language')
writeFiles(tcounts, 'technologies', 'Technology')
writeFiles(fcounts, 'features', 'Feature')
writeFiles(ccounts, 'contributors', 'Contributors')

# #! /usr/bin/env python
#
import json
import sys
import os
from collections import Counter
from jinja2 import *
import shutil

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': True
}

def run(context):
    # Load 101wiki into memory
    wiki = context.read_dump('wiki')['wiki']

    # Write .json and .html file -- the latter as a tag cloud
    def writeFiles(counts, label, prefix):

        # Write frequency map to JSON
        jsonFile = open(os.path.join(context.get_env('views101dir'), label + '.json'), 'w')
        jsonFile.write(json.dumps(counts, indent=4))

        # Prepare for buckets of scaling
        # Inspired by http://stackoverflow.com/questions/3180779/html-tag-cloud-in-python
        step = max(counts.values() or [0]) / 6

        counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)

        loader = FileSystemLoader(os.path.dirname(__file__))
        env = Environment(loader=loader)
        template = env.get_template('tagcloud.html')
        open(os.path.join(context.get_env('views101dir'), label + '.html'), 'w').write(template.render({
            'title': label,
            'counts': counts,
            'step': step,
            'root': 'http://101companies.org/wiki/' + prefix
        }))

    pages = wiki['pages']

    contributions = filter(lambda p: "Contribution" == p.get('p', ''), pages)

    uses = [p.get('Uses', []) for p in contributions]

    uses = [p for use in uses for p in use]

    uses = filter(lambda u: u['p'] == 'Language', uses)

    uses = [use['n'].replace('_', ' ') for use in uses]

    lcounts = Counter(uses)

    uses = [p.get('Uses', []) for p in contributions]
    uses = [p for use in uses for p in use]

    uses = list(filter(lambda u: u.get('p', '') == 'Technology', uses))

    uses = [use['n'] for use in uses]

    tcounts = dict(Counter(uses))

    writeFiles(lcounts, 'frequencyOfLanguages', 'Language')
    writeFiles(tcounts, 'frequencyOfTechnologies', 'Technology')

    css = os.path.join(os.path.dirname(__file__), 'wiki2tagclouds.css')
    shutil.copyfile(css, os.path.join(context.get_env('views101dir'), 'wiki2tagclouds.css'))

def test():
    pass

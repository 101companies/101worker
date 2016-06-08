#! /usr/bin/env python

import json
import sys
from collections import Counter
from jinja2 import *
import os
from functools import reduce

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': True,
    'behavior': {
        'uses': [['dump', 'wiki']]
    }
}

def run(context):
    # Load 101wiki into memory
    wiki = context.read_dump('wiki-links')

    # Write .json and .html file -- the latter as a tag cloud
    def writeFiles(counts, label, prefix):

        # Write frequency map to JSON
        jsonFile = open(os.path.join(context.get_env('views101dir'), label + '.json'), 'w')
        jsonFile.write(json.dumps(counts, indent=4))

    pages = wiki['wiki']['pages']

    contributions = filter(lambda p: "Contribution" == p.get('p', ''), pages)

    uses = [p.get('Uses', []) for p in contributions]
    uses = [p for use in uses for p in use]

    uses = list(filter(lambda u: u['p'] == 'Language', uses))

    uses = [use['n'].replace('_', ' ') for use in uses]

    lcounts = Counter(uses)

    uses = [p.get('uses', []) for p in contributions]
    uses = [p for use in uses for p in use]

    uses = filter(lambda u: u['p'] == 'Technology', uses)

    uses = [use['n'].replace('_', ' ') for use in uses]

    tcounts = dict(Counter(uses))

    # features

    implements = map(lambda c: c.get('implements', []), contributions)
    implements = list(reduce(lambda a, b: a+b, implements, []))

    features = filter(lambda o: o['p'] == 'Feature', implements)
    features = map(lambda o: o['n'], features, [])

    features = [f.replace('_', ' ') for f in features]

    fcounts = dict(Counter(features))

    #contributors

    developedBy = map(lambda c: c.get('developedBy', []), contributions)
    developedBy = list(reduce(lambda a, b: a+b, developedBy, []))

    developedBy = filter(lambda o: o['p'] == 'Contributor', developedBy)
    developedBy = map(lambda o: o['n'], developedBy, [])

    developedBy = filter(lambda n: n is not None, developedBy)

    developedBy = [d.replace('_', ' ') for d in developedBy]

    ccounts = dict(Counter(developedBy))

    writeFiles(lcounts, 'languages', 'Language')
    writeFiles(tcounts, 'technologies', 'Technology')
    writeFiles(fcounts, 'features', 'Feature')
    writeFiles(ccounts, 'contributors', 'Contributors')

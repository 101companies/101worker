#! /usr/bin/env python

import json
import sys

# Load 101wiki into memory

wiki = json.load(open(sys.argv[1], 'r'))

# Write .json and .html file -- the latter as a tag cloud
def writeFiles(counts, label, prefix):

    # Write frequency map to JSON
    jsonFile = open(label + '.json', 'w')
    jsonFile.write(json.dumps(counts))

    # Prepare for buckets of scaling
    # Inspired by http://stackoverflow.com/questions/3180779/html-tag-cloud-in-python
    step = max(counts.values()) / 6

    # Apply scaling and write HTML
    htmlFile = open(label + '.html', 'w')
    htmlFile.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">\n')
    htmlFile.write('<html>\n')
    htmlFile.write('<head>\n')
    htmlFile.write('  <title>' + label + '</title>\n')
    htmlFile.write('  <link rel="stylesheet" type="text/css" href="wiki2tagclouds.css"/>\n')
    htmlFile.write('</head>\n')
    htmlFile.write('<body>\n')

    root = 'http://101companies.org/index.php/' + prefix
    for tag, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        css = count / step        
        htmlFile.write('<a href="%s:%s" class="size-%s">%s</a>\n' % (root, tag, css, tag),)

    htmlFile.write('</body>\n')
    htmlFile.write('</html>\n')
    htmlFile.close()

# Collect counts for languages
lwiki = wiki["Language"]
lcounts = dict()
for l in lwiki:
    lcounts[lwiki[l]["name"]] = len(lwiki[l]["implementations"])

# Collect counts for technologies
twiki = wiki["Technology"]
tcounts = dict()
for t in twiki:
    tcounts[twiki[t]["name"]] = len(twiki[t]["implementations"])

writeFiles(lcounts, 'frequencyOfLanguages', 'Language')
writeFiles(tcounts, 'frequencyOfTechnologies', 'Technology')

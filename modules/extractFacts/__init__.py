#! /usr/bin/env python

import os
import sys
import json
import commands

config = {
    'wantdiff': True,
    'wantsfiles': True,
    'threadsafe': True
}

def run(context, change):
    if change['type'] == 'NEW_FILE':
        language = context.get_derived_resource(change['file'], '.lang')

        path = os.path.join('extractors', language, 'extractor')
        if os.path.exists(path):
            extractor = path
        else:
            extractor = None

        if extractor:
            source_file = os.path.join(context.get_env('repo101dir'), change['file'])
            command = "{0} < \"{1}\"".format(extractor, source_file)

            (status, output) = commands.getstatusoutput(command)

            context.write_derived_resource(change['file'], json.loads(output), '.extractor')

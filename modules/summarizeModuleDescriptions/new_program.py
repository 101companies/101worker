#! /usr/bin/env python

import json
import os
import sys
sys.path.append('../../libraries/101meta')
import const101

dump = {
    'file'  : {},
    'folder': [],
    'dump'  :[]
}

for root, dirs, files in os.walk('..'):
    for file in files:
        if 'module.json' == file:
            module = json.load(open(os.path.join(root, file), 'r'))
            for target in module.get('targets', []):
                dump[target['scope']][target['suffix']] = target

json.dump(dump, open(const101.tModuleSummaryDump, 'w'))
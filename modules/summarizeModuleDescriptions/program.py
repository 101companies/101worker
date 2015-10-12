#! /usr/bin/env python

import json
import os
import sys
sys.path.append('../../libraries/101meta')
import const101

dump = {
    'resource': { },
    'dump'    : { },
    'view'    : { }
}

for root, dirs, files in os.walk('..'):
    for file in files:
        if 'module.json' == file:
            module = json.load(open(os.path.join(root, file), 'r'))
            if 'targets' in module:
                moduleName = os.path.basename(root)
                for target in module['targets']:
                    dump[target['classifier']][target['suffix']] = {'name': moduleName, 'info': target}

json.dump(dump, open(const101.moduleSummaryDump, 'w'))



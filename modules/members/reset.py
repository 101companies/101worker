#! /usr/bin/env python

import os
import sys
import json

sys.path.append('../../libraries/101meta')
import const101

for dir in os.listdir(const101.tRoot):
    path = os.path.join(const101.tRoot, dir)
    if os.path.isdir(path):
        memberFile = os.path.join(path, 'members.json')
        if os.path.isfile(memberFile):
            print 'Removing {0}'.format(memberFile)
            os.remove(memberFile)
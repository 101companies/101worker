#!/usr/bin/env python

config = {
    'wantdiff': False,
    'wantsfiles': False,
    'threadsafe': False
}


import sys
sys.path.append('../libraries')

import meta101

def run(context):
    meta101.os.environ = context.get_env()

    meta101.matchall("matches", True)

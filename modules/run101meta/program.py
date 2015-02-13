#!/usr/bin/env python
from   argparse import ArgumentParser
import json
import os
import incremental101
import meta101


parser = ArgumentParser()
parser.add_argument('--phase', required=True, type=str, help="the 101meta "
                  + "rules phase (basics, predicates, fragments)")
phase = parser.parse_args().phase


path  = os.environ[phase + "101dump"]
rules = os.environ["rules101dump"]
args  = {"phasekey" : phase}

if os.path.exists(path):
    if os.path.getmtime(rules) > os.path.getmtime(path):
        args["entirerepo"] = True
    with open(path) as f:
        args["matches"   ] = json.load(f)["matches"]

dump = meta101.matchall(**args)

incremental101.writejson(path, dump)

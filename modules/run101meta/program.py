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


path = os.environ[phase + "101dump"]
args = [phase]

if os.path.exists(path):
    with open(path) as f:
        args.append(json.load(f)["matches"])

dump = meta101.matchall(*args)

incremental101.writejson(path, dump)

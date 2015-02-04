#!/usr/bin/env python
from   argparse import ArgumentParser
import os
import incremental101
import meta101


parser = ArgumentParser()
parser.add_argument('--phase', required=True, type=str, help="the 101meta "
                  + "rules phase (basics, predicates, fragments)")
args = parser.parse_args()


path = os.environ[args.phase + "101dump"]
dump = meta101.matchall(args.phase)

incremental101.writejson(path, dump)

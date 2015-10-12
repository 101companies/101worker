#! /usr/bin/env python

import os
import os.path
import sys
import json
sys.path.append('../../libraries/101meta')
import const101
import tools101

def fun(dirname, dirs, files):
   for basename in files:
      filename = os.path.join(dirname, basename)
      _, suffix = os.path.splitext(basename)
      if suffix in filesBySuffix:
         filesBySuffix[suffix] += [filename]
      else:
         filesBySuffix[suffix] = [filename]

print "Analyzing suffixes for 101repo."
dump = dict()
suffixes = json.load(open(const101.rulesDump, 'r'))["results"]["suffixes"]
filesBySuffix = dict()
tools101.loopOverFiles(fun, True)
filesBySuffix = filesBySuffix.items()
filesBySuffix = sorted(filesBySuffix, reverse=True, key=lambda (ext, list): len(list))
dump["suffixes"] = dict()
dump["suffixes"]["all"] = [ x[0] for x in filesBySuffix ]
dump["suffixes"]["matched"] = [ x[0] for x in filesBySuffix if x[0] in suffixes ]
dump["suffixes"]["unmatched"] = [ x[0] for x in filesBySuffix if not x[0] in suffixes ]
dump["filesBySuffix"] = dict()
dump["filesBySuffix"]["all"] = [ tools101.pair2json(x) for x in filesBySuffix ]
dump["filesBySuffix"]["matched"] = [ tools101.pair2json(x) for x in filesBySuffix if x[0] in suffixes ]
dump["filesBySuffix"]["unmatched"] = [ tools101.pair2json(x) for x in filesBySuffix if not x[0] in suffixes ]
dump["numbersBySuffix"] = dict()
dump["numbersBySuffix"]["all"] = [ tools101.pair2json((x, len(y))) for (x, y) in filesBySuffix ]
dump["numbersBySuffix"]["matched"] = [ tools101.pair2json((x, len(y))) for (x, y) in filesBySuffix if x in suffixes ]
dump["numbersBySuffix"]["unmatched"] = [ tools101.pair2json((x, len(y))) for (x, y) in filesBySuffix if not x in suffixes ]
dump["numbersOfSuffixes"] = dict()
dump["numbersOfSuffixes"]["all"] = len(dump["filesBySuffix"]["all"])
dump["numbersOfSuffixes"]["matched"] = len(dump["filesBySuffix"]["matched"])
dump["numbersOfSuffixes"]["unmatched"] = len(dump["filesBySuffix"]["unmatched"])
tools101.dump(dump,"numbersOfSuffixes")
suffixesFile = open(const101.suffixesDump, 'w')
suffixesFile.write(json.dumps(dump))
exit(0)

#! /usr/bin/env python

import os
import os.path
import sys
import json
sys.path.append('../../libraries/101meta')
import const101
import tools101

def readOrDefault(filename, default):
   try:
      return json.load(open(filename, 'r'))
   except IOError:
      return default

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
dump["files"] = dict()
dump["files"]["all"] = filesBySuffix
dump["files"]["matched"] = [ x for x in filesBySuffix if x[0] in suffixes ]
dump["files"]["unmatched"] = [ x for x in filesBySuffix if not x[0] in suffixes ]
dump["numbers"] = dict()
dump["numbers"]["all"] = len(dump["files"]["all"])
dump["numbers"]["matched"] = len(dump["files"]["matched"])
dump["numbers"]["unmatched"] = len(dump["files"]["unmatched"])
tools101.dump(dump)
suffixesFile = open(const101.suffixesDump, 'w')
suffixesFile.write(json.dumps(dump))
exit(0)

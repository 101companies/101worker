import os
import sys
import commands
import json
import const101


# Look up all metadata values, if any, for a certain metadata key
def valuesByKey(entry, key):
   return [ x[key]
                 for x in map(lambda u: u["metadata"], entry["units"])
                 if key in x ]


# Unambigious variation on valuesByKey
def valueByKey(entry, key):
   values = valuesByKey(entry, key)
   if len(values) != 1: return None
   return values[0]


# Dot-wise progress information
def tick():
    sys.stdout.write('.')
    sys.stdout.flush()


# Create target directory, if necessary
def makedirs(d):
   try:
      os.stat(d)
   except:
      try:
         os.makedirs(d)
      except OSError:
         pass

# Test whether a target is needed relative to a source
def build(sFilename, tFilename):
   try:
      sSize = os.stat(sFilename).st_size
      if sSize == 0:
         return False
      else:
         sCtime = os.path.getmtime(sFilename)
         tCtime = os.path.getmtime(tFilename)
         return sCtime > tCtime
   except:
      return True


# Run a command
def run(cmd):
   (status, output) = commands.getstatusoutput(cmd)
   if status != 0:
      print "Command failed: " + cmd
      print "Status: " + str(status)
      print "Output: " + output
   return (status, output)


def getBasics():
   matches = json.load(open(const101.matchesDump, 'r'))["matches"]
   result = dict()
   for match in matches:
      result[match["filename"]] = match
   return result


# Loop over matches
def mapMatches(
      testEntry # a predicate to select the file
    , testFiles # a predicate to test source and target file
    , suffix    # the extra suffix for target files
    , fun       # the function to apply to each match
    ):

    numberOfProblems = 0 # Number of problems
    numberOfSources = 0 # Number of source files
    noTargets = 0 # Number of (generated) target files
    matches = json.load(open(const101.matchesDump, 'r'))["matches"]

    for entry in matches:

       value = testEntry(entry)
       if value is None: continue
       numberOfSources += 1

       # RELATIVE dirname and filename
       rFilename = entry["filename"]
       rDirname = os.path.dirname(rFilename)
       basename = os.path.basename(rFilename)

       # SOURCE dirname and filename
       sDirname = os.path.join(const101.sRoot, rDirname)
       sFilename = os.path.join(sDirname, basename)

       # TARGET dirname and filename
       tDirname = os.path.join(const101.tRoot, rDirname)
       tFilename = os.path.join(tDirname, basename + suffix)

       # Generate file, if needed, and report problems, if any
       makedirs(tDirname)
       if not testFiles(sFilename, tFilename): continue
       noTargets += 1
       status = fun(value, rFilename, sFilename, tFilename)
       if status != 0: numberOfProblems += 1 

    sys.stdout.write('\n')
    dump = dict()
    dump["numbers"] = dict()
    dump["numbers"]["numberOfSources"] = numberOfSources
    dump["numbers"]["numberOfProblems"] = numberOfProblems
    return dump


# Loop over matches to handle specific metadata
def mapMatchesWithKey(
      key     # the key for metadata lookup
    , suffix  # the extra suffix for target files
    , fun     # the function to apply to each match
    ):

   def testEntry(entry):
      return valueByKey(entry, key)

   def testFiles(sFilename, tFilename):
      return build(sFilename, tFilename)
       
   return mapMatches(testEntry, testFiles, suffix, fun)


# Loop over all 101repo files
def loopOverFiles(fun, topdown):
    for root, dirs, files1 in \
            os.walk(os.path.join(const101.sRoot, "contributions"), topdown, None, False):
        if not root.startswith(os.path.join(const101.sRoot, ".git")+os.sep):
           dirname = root[len(const101.sRoot)+1:]
           files = [ f for f in files1 if not f in [".gitignore"] ]
           fun(dirname, dirs, files)

# Report to stdout
def dump(dump, special=None):
   if special in dump:
      print "\n"+special+":\n\t" + json.dumps(dump[special])
   if "numbers" in dump:
      print "\nnumbers:\n\t" + json.dumps(dump["numbers"])
   if "problems" in dump:
      print "\nproblems:\n\t" + json.dumps(dump["problems"])

import os
import sys
import commands
import json
import const101


# Look up all metadata values, if any, for a certain metadata key
def valuesByKey(units, key):
   return [ x[key] for x in map(lambda u: u["metadata"], units) if key in x ]


# Unambigious variation on valuesByKey
def valueByKey(units, key):
   values = valuesByKey(units, key)
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
def run(command):
   (status, output) = commands.getstatusoutput(command)
   if status != 0:
      print "Command failed: " + command
      print "Status: " + str(status)
      print "Output: " + output
   return (status, output)


# Look up matches and build map from filenames to matches
# TODO: Is this really needed (conceptually)?
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

   # Prepare house keeping
   global problems
   global numberOfFiles
   global numberOfSuccesses # to be initialized elsewhere for incrementality
   global numberOfFailures # to be initialized elsewhere for incrementality
   global numberOfInserts
   global numberOfUpdates
   global numberOfDeletes
   numberOfFiles = 0
   numberOfInserts = 0
   numberOfUpdates = 0
   numberOfDeletes = 0
   
   matches = json.load(open(const101.matchesDump, 'r'))["matches"]

   for entry in matches:

       value = testEntry(entry)
       if value is None: continue
       numberOfFiles += 1

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

       # Skip file, if possible
       makedirs(tDirname)
       if not testFiles(sFilename, tFilename): continue

       # Find and remove related problem
       failure = False
       idx = 0
       for p in problems:
          if p["filename"] == rFilename:
             del problems[idx]
             failure = True
             numberOfFailures -= 1
             break
          else:
             idx += 1
       exists = os.path.exists(tFilename)
       if not failure and exists:
          numberOfSuccesses -= 1

       # Generate target
       tick()
       result = fun(value, rFilename, sFilename, tFilename)

       # Housekeeping
       result["filename"] = rFilename
       if result["status"] != 0 or not os.path.exists(tFilename):
          numberOfFailures += 1
          problems.append(result)
       else:
          numberOfSuccesses += 1
       if not exists and os.path.exists(tFilename):
          numberOfInserts += 1
       elif exists and os.path.exists(tFilename):
          numberOfUpdates += 1
       elif exists and not os.path.exists(tFilename):
          numberOfDeletes += 1

   # Terminate ticking
   sys.stdout.write('\n')


# Derive targets by key
def deriveByKey(
      key     # the key for metadata lookup
    , suffix  # the extra suffix for target files
    , fun     # the function to apply to each match
    ):

   def testEntry(entry):
      return valueByKey(entry["units"], key)

   def testFiles(sFilename, tFilename):
      return build(sFilename, tFilename)
       
   return mapMatches(testEntry, testFiles, suffix, fun)


# Check sources by key
def checkByKey(
      key     # the key for metadata lookup
    , suffix  # the extra suffix for target files
    , check   # the function to apply to each match
    ):

   def derive(value, rFilename, sFilename, tFilename):
      result = check(value, rFilename, sFilename)
      tFile = open(tFilename, 'w')
      tFile.write(json.dumps(result))
      return result
       
   return deriveByKey(key, suffix, derive)


# Loop over all 101repo files
def loopOverFiles(fun, topdown):
    for root, dirs, files1 in \
            os.walk(os.path.join(const101.sRoot, "contributions"), topdown, None, False):
        if not root.startswith(os.path.join(const101.sRoot, ".git")+os.sep):
           dirname = root[len(const101.sRoot)+1:]
           files = [ f for f in files1 if not f in [".gitignore"] ]
           fun(dirname, dirs, files)


def beforeMapMatches(filename):
   global problems
   global numberOfSuccesses
   global numberOfFailures
   dump = dict()
   problems = list()
   numberOfSuccesses = 0
   numberOfFailures = 0

   # Incorporate previous dump, if any, into housekeeping
   try:
      dump = json.load(open(filename, 'r'))
      problems = dump["problems"]
      numberOfSuccesses = dump["numbers"]["numberOfSuccesses"]
      numberOfFailures = dump["numbers"]["numberOfFailures"]
   except IOError:
      pass

   return dump


def afterMapMatches(dump, filename=None):

   # Extend dump by generic information
   if not "numbers" in dump:
      dump["numbers"] = dict()
   dump["numbers"]["numberOfFiles"] = numberOfFiles
   dump["numbers"]["numberOfInserts"] = numberOfInserts
   dump["numbers"]["numberOfUpdates"] = numberOfUpdates
   dump["numbers"]["numberOfDeletes"] = numberOfDeletes
   dump["numbers"]["numberOfSuccesses"] = numberOfSuccesses
   dump["numbers"]["numberOfFailures"] = numberOfFailures
   dump["problems"] = problems

   releaseDump(dump, filename)

def releaseDump(dump, filename=None):
   # Print part of dump to stdout for the user's convenience
   if "numbers" in dump:
      print "\nnumbers:\n\t" + json.dumps(dump["numbers"])
   if "problems" in dump:
      print "\nproblems:\n\t" + json.dumps(dump["problems"])

   # Write dump to file and exit
   if not filename is None:
      dumpFile = open(filename, 'w')
      dumpFile.write(json.dumps(dump))

   sys.exit(0)


# Turn a list of shape [x,y] into a JSON object of shape { x : y }
def pair2json(x):
   assert len(x)==2
   result = dict()
   result[x[0]] = x[1]
   return result

# Turn a JSON object of shape { x : y } into one of shape { x : len(y) }
def list2len(x):
   assert len(keys(x))==1
   result = dict()
   result[x[0]] = x[1]
   return result

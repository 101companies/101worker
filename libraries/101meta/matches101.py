import os
import sys
import simplejson as json
import commands
import re
sys.path.append('../../libraries/101meta')
import const101
import tools101

#
# Build metadata unit
#
def buildUnit(units, id, metadata, result):
   unit = dict()
   unit["id"] = id
   unit["metadata"] = metadata
   if len(result)>0:
      for key in result:
         unit[key] = result[key]
   units.append(unit)


#
# Handle filename, basename, and dirname constraints alike
#
def checkFilename(rule, key, value):
   if not key in rule:
      return True
   else:
      either = False
      values = rule[key]
      if not isinstance(values, list): values = [ values ]
      for pattern in values:
         if pattern[0] != "#" or pattern[len(pattern)-1] != "#":
            if value == pattern:
               either = True
               break
            if key=="dirname":
               if value.startswith(pattern+"/"):
                  either = True
                  break
         else:
            global noPatternConstraints
            noPatternConstraints += 1
            pattern = pattern[1:len(pattern)-2]
            match = re.search(pattern, value)
            if key=="dirname":
               if value[match.end()+1] != '/':
                  match = None
            if not match is None:
               either = True
               global noPatternConstraintsOk
               noPatternConstraintsOk += 1
               break
      return either

#
# Try one rule for the given file
#
def matchFile(phase, dirname, basename, rule):

   result = dict()
   filename = os.path.join(dirname, basename)

   #
   # Check applicability of rule to phase
   #      
   if ("predicate" in rule and phase != "predicates")\
   or ("fragment" in rule and phase != "fragments")\
   or (not "predicate" in rule and phase == "predicates")\
   or (not "fragment" in rule and phase == "fragments"):
      return None

   #
   # Check dirname constraint
   #      
   if not checkFilename(rule, "dirname", dirname):
      return None
   
   #
   # Check basename constraint
   #
   if not checkFilename(rule, "basename", basename):
      return None

   #
   # Check filename constraint
   #
   if not checkFilename(rule, "filename", filename):
      return None

   #
   # Check suffix constraint
   #      
   if "suffix" in rule:
      suffixes = rule["suffix"]
      if not isinstance(suffixes, list): suffixes = [ suffixes ]
      either = False
      for suffix in suffixes:
         if basename.endswith(suffix):
            either = True
            break
      if not either: return None

   #
   # Check content, if required.
   #
   if "content" in rule:
      global noContentConstraints
      noContentConstraints += 1
      pattern = rule["content"]
      if pattern[0]=="#" and pattern[len(pattern)-1]=="#":
         pattern = pattern[1:len(pattern)-2]
      content = open(os.path.join(const101.sRoot, filename), 'r').read()
      searchResult = re.search(pattern, content)
      if searchResult is None:
         return None
      else:
         global noContentConstraintsOk
         noContentConstraintsOk += 1
         
   #
   # Apply predicate, if present.
   #
   if "predicate" in rule:
      predicate = rule["predicate"]
      global predicates
      predicates.add(predicate)
      global noPredicateConstraints
      noPredicateConstraints += 1
      if "args" in rule:
         args = rule["args"]
         if not isinstance(args, list): args = [ args ]
      else:
         args = []
      cmd = os.path.join(const101.sRoot, predicate)
      for arg in args:
         cmd += " \"" + arg + "\""
      cmd += " \"" + os.path.join(const101.sRoot, filename) + "\""
      (status, output) = commands.getstatusoutput(cmd)
      if status == 0:
         global noPredicateConstraintsOk
         noPredicateConstraintsOk += 1
      else:
         return None

   #
   # Locate fragment, if present.
   #
   if "fragment" in rule:
      fragment = rule["fragment"]
      global noFragments
      noFragments += 1
      if "args" in rule:
         args = rule["args"]
         if not isinstance(args, list): args = [ args ]
      else:
         args = []
      locator = None
      if filename in basics:
         locator = tools101.valueByKey(basics[filename], "locator")
      if locator is None:
         failure = dict()
         failure["error"] = "locator not found"
         failure["rule"] = rule
         failures.append(failure)
         return None
      global locators
      locators.add(locator)
      cmd = os.path.join(const101.sRoot, locator)
      tmpIn = os.path.join(const101.tRoot, filename + ".tmpIn")
      tmpOut = os.path.join(const101.tRoot, filename + ".tmpOut")
      for arg in args:
         cmd += " \"" + arg + "\""
      cmd += " \"" + os.path.join(const101.sRoot, filename) + "\""
      cmd += " \"" + tmpIn + "\""
      cmd += " \"" + tmpOut + "\""
      tmpInFile = open(tmpIn, 'w')
      if isinstance(fragment, basestring):
         tmpInContent = fragment
      else:
         tmpInContent = json.dumps(fragment)
      tmpInFile.write(tmpInContent)
      tmpInFile.close()
      (status, output) = commands.getstatusoutput(cmd)
      if status == 0:
         try:
            pass
#            os.remove(tmpIn)
         except:
            pass
         try:
            tmpOutFile = open(tmpOut, 'r')
            result["lines"] = json.load(open(tmpOut, 'r'))
         except:
            failure = dict()
            failure["locator"] = locator
            failure["command"] = cmd
            failure["output"] = "result of fragment location not found"
            failure["rule"] = rule
            failures.append(failure)
            return None
         try:
            pass
#            os.remove(tmpOut)
         except:
            pass
      if status != 0:
         failure = dict()
         failure["locator"] = locator
         failure["command"] = cmd
         failure["status"] = status
         failure["output"] = output
         failure["rule"] = rule
         failures.append(failure)
         return None


   #
   # No constraint left to check
   #
   return result


#
# Try all rules for the given file and build metadata units
#
def handleFile(phase, dirname, basename, suffix):
   filename = os.path.join(dirname, basename)
   units = list() # metadata units for the file at hand
   id = 0 # current rule number
   for r in rules:
      rule = r["rule"]
      result = matchFile(phase, dirname, basename, rule)
      if not result is None:      
         if "metadata" in rule:
            metadata = rule["metadata"]
            if isinstance(metadata, list):
               for m in metadata:
                  buildUnit(units, id, m, result)                    
            else:
               buildUnit(units, id, metadata, result)
      id += 1

   # Contract units to pay attention to dominators
   keys = list()
   removals = list()
   for unit in units:
      metadata = unit["metadata"]
      if "dominator" in metadata:
         keys.append(metadata["dominator"])
   for key in keys:      
      for unit in units:
         metadata = unit["metadata"]
         if key in metadata \
         and (not "dominator" in metadata
              or not metadata["dominator"] == key):
            removals.append(unit)
   survivals = list()
   for unit in units:
      if not unit in removals:
         survivals.append(unit)
   units = survivals
            
   # Add entry to matches if any matches for file at hand
   tools101.makedirs(os.path.join(const101.tRoot, dirname))
   tFilename = os.path.join(const101.tRoot, dirname, basename + suffix)
   matchesFile = open(tFilename, 'w')
   matchesFile.write(json.dumps(units))
   if len(units) > 0:
      global noUnits
      global noFiles
      noUnits += len(units)
      noFiles += 1
      entry = dict()
      entry["filename"] = filename
      entry["units"] = units
      matches.append(entry)
      tools101.tick()


#
# Process all rules and files
#
def matchAll(phase, suffix):
    global basics
    global rules
    global matches
    global failures
    global predicates
    global locators
    global noFiles
    global noUnits
    global noPatternConstraints
    global noPatternConstraintsOk
    global noContentConstraints
    global noContentConstraintsOk
    global noPredicateConstraints
    global noPredicateConstraintsOk
    global noFragments
    if (phase!="basics"):
       basics = tools101.getBasics()
    rules = json.load(open(const101.rulesDump, 'r'))["rules"]
    matches = list()
    failures = list()
    predicates = set()
    locators = set()
    noFiles = 0
    noUnits = 0
    noPatternConstraints = 0
    noPatternConstraintsOk = 0 
    noContentConstraints = 0
    noContentConstraintsOk = 0
    noPredicateConstraints = 0
    noPredicateConstraintsOk = 0 
    noFragments = 0
    print "Matching 101meta metadata on 101repo (phase \"" + str(phase)+ "\")."
    for root, dirs, files in os.walk(os.path.join(const101.sRoot, "contributions")):
        if not root.startswith(os.path.join(const101.sRoot, ".git")+os.sep):
            for basename in files:
                if not basename in [".gitignore"]:
                    dirname = root[len(const101.sRoot)+1:]
                    handleFile(phase, dirname, basename, suffix)
    sys.stdout.write('\n')
    mr = dict()
    mr["matches"] = matches
    mr["failures"] = failures
    mr["rules"] = rules
    if phase=="predicates":
       mr["predicates"] = list(predicates)
    if phase=="fragments":
       mr["locators"] = list(locators)
    print str(noFiles) + " files affected."
    print str(len(failures)) + " failures encountered."
    print str(noUnits) + " metadata units attached."
    print str(noContentConstraints) + " content constraints checked."
    print str(noContentConstraintsOk) + " content constraints succeeded."
    print str(noPatternConstraints) + " filename-pattern constraints checked."
    print str(noPatternConstraintsOk) + " filename-pattern constraints succeeded."
    if phase=="predicates":
       print str(noPredicateConstraints) + " predicate constraints checked."
       print str(noPredicateConstraintsOk) + " predicate constraints succeeded."
    if phase=="fragments":
       print str(len(locators)) + " fragment locators exercised."
       print str(noFragments) + " fragment descriptions checked."
    return mr

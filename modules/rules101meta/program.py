#! /usr/bin/env python
import os
import fnmatch
import json
import incremental101


# Check rule for validity
def validRule(rule):
    return True

# Normalize rule
def normalizeRule(rule):
    if not isinstance(rule["metadata"], list):
        rule["metadata"] = [ rule["metadata"] ]

# Gather metrics
def countRule(rule):

    global suffixes
    if "suffix" in rule:
        suffix = rule["suffix"]
        if not suffix in suffixes:
            suffixes += [suffix]

    global predicates
    if "predicate" in rule:
        predicate = rule["predicate"]
        if not predicate in predicates:
            predicates[predicate] = []
        if not "args" in rule:
            args = []
        else:
            args = rule["args"]
            if not isinstance(args, list):
                args = [args]
        for arg in args:
            if not arg in predicates[predicate]:
                predicates[predicate] += [arg]


#
# Gather metrics.
# Check validity upfront.
# Qualify rule with origin information.
#
def handleRule(rule):
    countRule(rule)
    if validRule(rule):
        normalizeRule(rule)
        entry = dict()
        entry['filename'] = rFilename
        entry['rule'] = rule
        rules.append(entry)
    else:
        invalidFiles.append(rFilename)

print "Gathering 101meta rules from 101repo."

# Prepare dump
results = dict()
rules = list()
suffixes = list()
predicates = dict()
results["rules"] = rules
results["suffixes"] = suffixes
results["predicates"] = predicates

problems = dict()
unreadableFiles = list()
invalidFiles = list()
problems["unreadableFiles"] = unreadableFiles
problems["invalidFiles"] = invalidFiles

numbers = dict()
numberOfFiles = 0

dump = dict()
dump["results"] = results
dump["problems"] = problems
dump["numbers"] = numbers

# Main loop
repo101dir = os.environ["repo101dir"]
for root, dirs, files in os.walk(repo101dir, followlinks=True):
    for basename in fnmatch.filter(files, "*.101meta"):
        filename = os.path.join(root, basename)
        print filename
        rFilename = filename[len(repo101dir) + 1:] # relative file name
        numberOfFiles += 1

        # Shield against JSON encoding errors
        try:
            jsonfile = open(filename, "r")
            data = json.load(jsonfile)

            # Handle lists of rules
            if isinstance(data, list):
                for rule in data:
                    handleRule(rule)
            else:
                handleRule(data)
            break

        except json.decoder.JSONDecodeError:
            print "Unreadable file: " + rFilename + " (JSONDecodeError)"
            unreadableFiles.append(rFilename)

# Completion of dump
numbers["numberOfRules"] = len(rules)
numbers["numberOfProblems"] = len(unreadableFiles) + len(invalidFiles)
numbers["numberOfSuffixes"] = len(suffixes)
numbers["numberOfPredicates"] = len(predicates)

incremental101.writejson(os.environ["rulesDump101"], dump)

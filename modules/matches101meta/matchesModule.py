#! /usr/bin/env python


import os
import json
from matchesCore import handleFile
from tools import *
sys.path.append('../../libraries/101meta')
import const101

#load rules
rules = json.load(open(const101.rulesDump))["results"]["rules"]

#create the dump (a new dump so I can compare with the old dump and search for errors)
dump = ModuleDump('/Daten/101companies/101web/data/dumps/matches_new.json')
dump.matches  = []
dump.failures = []
dump.rules    = rules


def matchingFunc(sFile, tFile):
    global rules
    global dump

    #incremental check
    if build(sFile, tFile):
        #.matches.json file needs to be created
        dirname = os.path.dirname(sFile)
        basename = os.path.basename(sFile)

        #deleting part of the dirname is necessary because of the "filename" constraint
        units = handleFile('basics', dirname[len(const101.sRoot) + 1:], basename, rules)

        makedirs(os.path.dirname(tFile))
        json.dump(units, open(tFile, 'w'))
    else:
        #an current matches.json file exists
        units = json.load(open(tFile, 'r'))

    #updating dump
    if len(units) > 0:
        dump.matches.append({
                'units' : units,
                'filename': sFile.replace(const101.sRoot, '')
            })

    tick()



### MAIN PROGRAM ###
print 'Matching 101meta metadata on 101repo'
#actual loop
loopOverDir(const101.sRoot, const101.tRoot, '.matches.json', matchingFunc)

#contains inbuild checking if writing is necessary
dump.write()

#str(dump) is currently only useful if the keys "problems" or "numbers" exist
print '\nMatching finished\n' + str(dump)

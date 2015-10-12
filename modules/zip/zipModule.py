#! /usr/bin/env python

import os
import sys
from distutils.archive_util import make_zipfile

sys.path.append('../../libraries/101meta')
import const101


### GENERAL ###
def ensureFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def zipFolder(source, target):
    #os.chdir(source)
    #make_zipfile(target, "./")
    os.chdir(os.path.dirname(source))
    make_zipfile(target, './' + os.path.basename(source))

### SPECIFIC ###
#zip all contributions in single files
def zipContributions():
    print "zipping single contribs"
    dirlist = os.listdir(contrib)
    for d in dirlist:
        source = os.path.join(contrib, d)
        if os.path.isdir(source):
            target = os.path.join(contribZips, d)
            zipFolder(source, target)

#zip 101repo folder
def zip101Repo():
    print "zipping 101repo folder"
    source = repo
    target = os.path.join(webZip, "101repo")
    zipFolder(source, target)

#zipping dumps
def zipDumps():
    print "zipping dumps folder"
    source = os.path.join(web, "dumps")
    target = os.path.join(webZip, "dumps")
    zipFolder(source, target)

#zipping resources
def zipResources():
    print "zipping resources folder"
    source = os.path.join(web, "resources")
    target = os.path.join(webZip, "resources")
    zipFolder(source, target)


### MAIN PROGRAMM ###
#set folders
web = os.path.abspath("../../../101web/data")
webZip = os.path.join(web, "zips");
contribZips = os.path.join(webZip, "contributions")

repo = os.path.abspath(const101.sRoot)
#contrib = os.path.abspath(os.path.join(const101.sRoot, "contributions"))
contrib = os.path.join(repo, "contributions")

#create folders if necessary
ensureFolder(webZip)
ensureFolder(contribZips)

#zipping the different parts
zipContributions()
zip101Repo()

zipDumps()
zipResources()


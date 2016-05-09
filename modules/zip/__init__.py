#! /usr/bin/env python

import os
import sys
from distutils.archive_util import make_zipfile

config = {
    'wantdiff': False
}

### GENERAL ###
def ensureFolder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)


def zipFolder(source, target):
    os.chdir(os.path.dirname(source))
    make_zipfile(target, './' + os.path.basename(source))

### SPECIFIC ###
#zip all contributions in single files
def zipContributions():
    print("zipping single contribs")
    dirlist = os.listdir(contrib)
    for d in dirlist:
        source = os.path.join(contrib, d)
        if os.path.isdir(source):
            target = os.path.join(contribZips, d)
            zipFolder(source, target)

#zip 101repo folder
def zip101Repo():
    print("zipping 101repo folder")
    source = repo
    target = os.path.join(webZip, "101repo")
    zipFolder(source, target)

#zipping dumps
def zipDumps():
    print("zipping dumps folder")
    source = os.path.join(web, "dumps")
    target = os.path.join(webZip, "dumps")
    zipFolder(source, target)

#zipping resources
def zipResources():
    print("zipping resources folder")
    source = os.path.join(web, "resources")
    target = os.path.join(webZip, "resources")
    zipFolder(source, target)

def run(context):
    global contrib
    global web
    global webZip
    global contribZips
    global repo

    ### MAIN PROGRAMM ###
    #set folders
    web = os.path.abspath(context.get_env('data101dir'))
    webZip = os.path.join(web, "zips")
    contribZips = os.path.join(webZip, "contributions")

    repo = context.get_env('repo101dir')
    contrib = os.path.join(repo, "contributions")

    #create folders if necessary
    ensureFolder(webZip)
    ensureFolder(contribZips)

    #zipping the different parts
    zipContributions()
    zip101Repo()

    zipDumps()
    zipResources()

import unittest
from unittest.mock import patch, Mock

class ZipTest(unittest.TestCase):

    @patch('modules.zip.zipFolder')
    @patch('modules.zip.ensureFolder')
    @patch('modules.zip.zipContributions')
    def test_run(self, zipContributions, ensureFolder, zipFolder):
        env = Mock(**{ 'get_env.return_value': '/some/path/' })
        run(env)

        zipFolder.assert_any_call('/some/path/', '/some/path/zips/101repo')
        zipFolder.assert_any_call('/some/path/dumps', '/some/path/zips/dumps')
        zipFolder.assert_any_call('/some/path/resources', '/some/path/zips/resources')

        ensureFolder.assert_any_call('/some/path/zips')
        ensureFolder.assert_any_call('/some/path/zips/contributions')

def test():
    suite = unittest.TestLoader().loadTestsFromTestCase(ZipTest)
    unittest.TextTestRunner(verbosity=2).run(suite)

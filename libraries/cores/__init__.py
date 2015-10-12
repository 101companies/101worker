#! /usr/bin/env python

import os
import json
import sys

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

def write(tFile, data):
    makedirs(os.path.dirname(tFile))
    json.dump(data, open(tFile, 'w'))

# Test whether a target is needed relative to a source
def build(sFilename, tFilename):
    try:
        #commented out, because some library files where returning 0 even though they shouldn't
        #sSize = os.stat(sFilename).st_size
        #if sSize == 0:
        #    return False
        #else:
        sMTime = os.path.getmtime(sFilename)
        tMTime = os.path.getmtime(tFilename)
        return sMTime > tMTime
    except:
        return True


def loopOverDir(sourceDir, targetDir, suffix, logicFunc):
    for root, dirs, files in os.walk(sourceDir):
        for file in files:
            if not '.git' in file and not '.git' in root:
                sFile = os.path.join(root, file)
                tFile = os.path.join(root.replace(sourceDir, targetDir), file + suffix)
                logicFunc(sFile, tFile)


class ModuleDump:
    def __init__(self, filename=None):
        self.__dict__['_filename'] = filename
        self.__dict__['_dump'] = {}

    def __str__(self):
        str = ''
        if 'numbers' in self._dump:
            str += '\nnumbers:\n\t' + json.dumps(self._data['numbers'])
        if 'problems' in self._dump:
            print '\nproblems:\n\t' + json.dumps(self._dump['problems'])

        return str

    def __getattr__(self, item):
        return self._dump.get(item, None)

    def __setattr__(self, key, value):
        self._dump[key] = value

    def _writeNecessary(self):
        try:
            existingDump = json.load(open(self._filename, 'r'))
            if existingDump == self._dump:
                return False
            return True
        except:
            return True


    def write(self, force=False):
        """
        Writes the dump into a file. In standard mode, it first checks whether writing is necessary (to allow incremental
        file creation)
        :param force: bool indicating whether writing can be omitted, if it isn't necessary
        """
        if not self._filename is None:
            if force or self._writeNecessary():
                dumpFile = open(self._filename, 'w')
                dumpFile.write(json.dumps(self._dump, indent=4))
                dumpFile.close()

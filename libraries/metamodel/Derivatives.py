__author__ = 'martin'

import os
import json
import sys
import types
import urllib2

from Exceptions import *

import helpers

sys.path.append('../101meta')
sys.path.append('..')
import const101


#abstract class
class Derivative:
    def __init__(self, relativePath):

        if self.__class__.__name__ == 'Derivative':
            raise NotImplementedError('This class is abstract')

        if USE_EXPLORER_SERVICE:
            self.__path = os.path.join(const101.url101data, 'resources', relativePath)
            self.__loadFromWeb()
        else:
            self.__path = os.path.join(const101.tRoot, relativePath)
            self.__exists = os.path.exists(self.__path)

    @property
    def path(self):
        return self.__path

    @property
    def exists(self):
        return self.__exists

    @property
    def rawData(self):
        if not '_Derivative__raw_data' in self.__dict__:
            if not self.exists:
                raise NonExistingPathException(self.path)
            self.__raw_data = json.load(open(self.path, 'r'))

        return self.__raw_data

    def __loadFromWeb(self):
        try:
            self.__raw_data = helpers.loadJSONFromUrl(self.path)
        except:
            self.__exists = False

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.path


class Metrics(Derivative):
    def __init__(self, identifier):
        Derivative.__init__(self, identifier + '.metrics.json')


class Meta101(Derivative):
    def select(self, filterFunc):
        for entry in self.rawData:
            entry = entry['metadata']
            if not isinstance(entry, types.ListType):
                entry = [ entry ]
            for e in entry:
                if filterFunc(e):
                    return e


class Matches(Meta101):
    def __init__(self, identifier):
        Derivative.__init__(self, identifier + '.matches.json')


class Extractor(Derivative):
    def __init__(self, identifier):
        Derivative.__init__(self, identifier+'.extractor.json')

    def selectFragment(self, fragmentDescription, fragmentData=None):
        #necessary beacuse empty for an empty list, "if not fragmentData" would also yield true
        if fragmentData == None:
            fragmentData = self.rawData['fragments']

        if not fragmentDescription or fragmentDescription == '':
            return fragmentData

        parts = fragmentDescription.split('/')
        classifier, fragmentName, index = parts[0], parts[1], None
        remainingDescription = '/'.join(parts[2:])

        if len(parts) > 2 and parts[2].isdigit():
            index = int(parts[2])
            remainingDescription = os.path.join(parts[3:])

        for fragment in fragmentData:
            if fragment['classifier'] == classifier and fragment['name'] == fragmentName and (index == None or fragment.get('index', 0) == index):
                return self.selectFragment(remainingDescription, fragment.get('fragments', []))

        raise BadFragmentDescription()



__author__ = 'martin'

import os
import json

import helpers

class PullRepoDump():
    def __init__(self):
        if USE_EXPLORER_SERVICE:
            self.__loadFromWeb()

    @property
    def rawData(self):
        if not '_PullRepoDump__raw_data' in self.__dict__:
            self.__raw_data = json.load(open(const101.pullRepoDump, 'r'))

        return self.__raw_data

    def getGithubLink(self, memberName):
        if not memberName in self.rawData:
            raise Exception('no clue which exception, but member is not in pullrepo dump')
        return self.rawData[memberName]

    def __loadFromWeb(self):
        self.__raw_data = helpers.loadJSONFromUrl(os.path.join(const101.url101data, 'dumps', 'PullRepo.json'))


class WikiDump():
    def __init__(self):
        if USE_EXPLORER_SERVICE:
            self.__loadFromWeb()

    def rawData(self):
        if not '_WikiDump__raw_data' in self.__dict__:
            self.__raw_data = json.load(open(const101.wikiDump, 'r'))

        return self.__raw_data

    def __loadFromWeb(self):
        self.__raw_data = helpers.loadJSONFromUrl(os.path.join(const101.url101data, 'dumps', 'wiki.json'))
__author__ = 'martin'

import os
import json
import sys

sys.path.append('../101meta')
sys.path.append('..')
import helpers
import const101
import mediawiki


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


#Abstract Base class with functionality for raw data
class Dump():
    __metaclass__ = Singleton

    def __init__(self, dumpName):
        self.__dumpName = dumpName
        self.__path = os.path.join(const101.dumps, dumpName)
        if USE_EXPLORER_SERVICE:
            self.__path = os.path.join(const101.url101data, 'dumps', self.__dumpName)
            self.__loadFromWeb()

    @property
    def path(self):
        return self.__path

    @property
    def rawData(self):
        if not '_Dump__raw_data' in self.__dict__:
            self.__raw_data = json.load(open(os.path.join(const101.dumps, self.__dumpName)))

        return self.__raw_data

    def __loadFromWeb(self):
        self.__raw_data = helpers.loadJSONFromUrl(self.path)


#Concrete subclasses
class PullRepoDump(Dump):
    def __init__(self):
        Dump.__init__(self, 'PullRepo.json')

    def getGithubLink(self, memberName):
        return self.rawData.get(memberName, None)


class WikiDump(Dump):
    def __init__(self):
        Dump.__init__(self, 'wiki.json')
        self.__curPage = -1
        self.__maxPages = len(self.rawData['wiki']['pages'])

    def selectPage(self, namespace, title):
        for page in self.rawData['wiki']['pages']:
            if page.get('p', None) == namespace and page.get('n', None) == title:
                return page

        return None

    def getHeadline(self, namespace, title):
        page = self.selectPage(namespace, title)
        if page:
            return mediawiki.remove_headline_markup(page.get('headline', ''))

        return None

    def __iter__(self):
        return self

    def next(self):
        if (self.__curPage+1) == self.__maxPages:
            self.__curPage = -1
            raise StopIteration
        else:
            self.__curPage += 1
            return self.rawData['wiki']['pages'][self.__curPage]


def main():
    #introducing the variable, as it's not available if i just debug this file
    global USE_EXPLORER_SERVICE
    USE_EXPLORER_SERVICE = False

    #--------------------------
    #normal code
    for page in WikiDump():
        print page

    print WikiDump().getHeadline('Contribution', 'antlrLexer')


if __name__ == '__main__':
    main()

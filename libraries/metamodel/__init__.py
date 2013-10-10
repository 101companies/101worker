# 101companies metamodel API
#
# A API that can be used to code against 101companies files
#
#      class    | state
#   ------------+----------
#   Namespace   | documentation needed
#   Folder      | documentation needed
#   Member      | documentation needed
#   File        | v1 FINISHED
#   Fragment    | documentation needed
#
# current problems / discussion points:
#   - Fragments currently expect the .extractor.json derivative instead of executing the fact extractor themselves.
#       Possibly problematic if module is broken
#
# Pointers for implementation:
# * HTTP or filesystem access / switchable by config variable
# * Backlinks should be implemented (parent and "root"/"member")
# * Highest namespace has ID "namespaces"
# * when returning derivatives, return all that are possibly there


# normal Python imports
import os
import json
import sys
import types
import re
import commands

# state variable for HTTP/filesystem access
import __builtin__

__builtin__.USE_EXPLORER_SERVICE = False

#importing other parts of metamodel API
import helpers
from Exceptions import *
from Derivatives import *
from Dumps import *

#importing other 101 libraries
sys.path.append('../101meta')
sys.path.append('..')
import const101
from mediawiki import wikifyNamespace
from mediawiki import dewikifyNamespace




# Helper functions
def useWebInterface():
    __builtin__.USE_EXPLORER_SERVICE = True

class walk:
    def __init__(self, root):
        if isinstance(root, Namespace):
            self.__stack = root.members
        else:
            self.__stack = [ root ]

    def __iter__(self):
        return self

    def next(self):
        if len(self.__stack) == 0:
            raise StopIteration

        cur = self.__stack.pop(0)
        self.__stack = cur.folders + self.__stack

        return cur.folders, cur.files

# normal API
class Namespace:
    def __init__(self, identifier, parent=None):
        self.__identifier = identifier
        relPath = identifier
        if identifier == 'namespaces':
            relPath = ''

        if USE_EXPLORER_SERVICE:
            self.__sPath = os.path.join(const101.url101explorer, relPath)
            self.__loadFromWeb()
        else:
            self.__sPath = os.path.join(const101.sRoot, relPath)
            self.__tPath = os.path.join(const101.tRoot, relPath)
            if self.name != 'Namespace' and not self.name in json.load(open(os.path.join(const101.tRoot, 'members.json'), 'r')):
                raise BadIdentifierException(self.identifier)

    @property
    def identifier(self):
        return self.__identifier

    @property
    def name(self):
        if not '_Namespace__name' in self.__dict__:
            self.__name = wikifyNamespace(self.identifier)
        return self.__name

    @property
    def path(self):
        return self.__sPath

    @property
    def classifier(self):
        return 'Namespace'

    @property
    def parent(self):
        if not '_Namespace__parent' in self.__dict__:
            if self.identifier == 'namespaces':
                self.__parent = None
            else:
                self.__parent = Namespace('namespaces')
        return self.__parent

    @property
    def headline(self):
        if not '_Namespace__headline' in self.__dict__:
            self.__headline = WikiDump().getHeadline('Namespace', self.name)
        return self.__headline

    @property
    def endpointLink(self, format='json'):
        if not '_Namespace__endpoint' in self.__dict__:
            self.__endpoint = os.path.join(const101.url101endpoint, 'Namespace:' + self.name, format)
        return self.__endpoint

    @property
    def wikiLink(self):
        if not '_Namespace__wiki' in self.__dict__:
            self.__wiki = os.path.join(const101.url101wiki, 'Namespace' + ':' + self.name)
        return self.__wiki

    @property
    def github(self):
        if not '_Namespace__github' in self.__dict__:
            relPath = self.identifier
            if self.identifier == 'namespaces':
                relPath = ''
            self.__github = os.path.join(const101.url101repo, relPath)
        return self.__github

    @property
    def members(self):
        if not '_Namespace__members' in self.__dict__:
            self.__members = []
            if not '_Namespace__memberIds' in self.__dict__:
                self.__memberIds = [os.path.join(self.identifier, mId) for mId in json.load(open(os.path.join(self.__tPath, 'members.json')))]
            for id in self.__memberIds:
                if self.identifier == 'namespaces':
                    self.__members.append(Namespace(id, parent=self))
                else:
                    self.__members.append(Member(id, parent=self))

        return self.__members

    def __loadFromWeb(self):
        data = helpers.loadJSONFromUrl(self.path)

        self.__wiki = data['wiki']
        self.__github = data['github']
        self.__headline = data['headline']
        self.__endpoint = data['endpoint']

        self.__memberIds = []
        for id in data['members']:
            if self.identifier == 'namespaces':
                self.__memberIds.append(id['resource'].replace(const101.url101explorer, ''))
            else:
                self.__memberIds.append(id['resource'].replace(const101.url101explorer, ''))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(Namespace, {})'.format(self.__identifier)

    def __eq__(self, other):
        if hasattr(other, 'identifier'):
            return other.identifier == self.identifier
        return NotImplemented

class Folder:
    def __init__(self, identifier, member=None, parent=None):
        self.__identifier = identifier
        parts = identifier.split('/')

        if USE_EXPLORER_SERVICE:
            self.__sPath = os.path.join(const101.url101explorer, identifier)
            try:
                self.__loadFromWeb()
            except urllib2.HTTPError:
                raise BadIdentifierException(self.identifier)
        else:
            #create paths
            self.__sPath = os.path.join(const101.sRoot, identifier)
            self.__tPath = os.path.join(const101.tRoot, identifier)

            if not isinstance(self, Member):
                if not os.path.exists(self.__sPath):
                    raise BadIdentifierException(identifier)
                if len(parts) <= 2:
                    raise BadIdentifierException(identifier, '{} doesn\'t identify a Folder, but rather a Member')

        self.__name = parts[-1]

    @property
    def identifier(self):
        return self.__identifier

    @property
    def name(self):
        return self.__name

    @property
    def path(self):
        return self.__sPath

    @property
    def classifier(self):
        return 'Folder'

    @property
    def member(self):
        """
        returns a backlink to the member this file belongs to
        :return: instance of Member class
        """
        if not '_Folder__member' in self.__dict__:
            self.__member = Member('/'.join(self.identifier.split('/')[0:2]))
        return self.__member

    @property
    def parent(self):
        """
        returns a backlink to the folder this file belongs to
        :return: instance of folder or member class, depending on where this file is sitting in the file tree
        """
        if not '_Folder__parent' in self.__dict__:
            pIdentifier = self.identifier.rsplit('/', 1)[0]
            if pIdentifier == self.member.identifier:
                self.__parent = self.member
            else:
                self.__parent = Folder(pIdentifier)

        return self.__parent

    @property
    def folders(self):
        if not '_Folder__folders' in self.__dict__:
            self.__folders = []
            if not hasattr(self, 'virtual') or not self.virtual:
                if not '_Folder__folderIds' in self.__dict__:
                    self.__folderIds = [os.path.join(self.identifier, o)
                                        for o in os.listdir(self.path)
                                        if os.path.isdir(os.path.join(self.path, o))
                    ]

                self.__folders = [Folder(identifier, member=self.member, parent=self.parent)
                                  for identifier in self.__folderIds
                ]

        return self.__folders

    @property
    def files(self):
        if not '_Folder__files' in self.__dict__:
            self.__files = []
            if not hasattr(self, 'virtual') or not self.virtual:
                if not '_Folder__fileIds' in self.__dict__:
                    self.__fileIds = [os.path.join(self.identifier, o)
                                      for o in os.listdir(self.path)
                                      if os.path.isfile(os.path.join(self.path, o))
                    ]

                self.__files = [File(identifier, member=self.member, parent=self.parent)
                                for identifier in self.__fileIds
                ]

        return self.__files

    @property
    def derivatives(self):
        return []

    @property
    def github(self):
        if not '_Folder__github' in self.__dict__:
            self.__github = self.parent.github + '/' + self.name

        return self.__github

    def __loadFromWeb(self):
        data = helpers.loadJSONFromUrl(self.__sPath)

        self.__github = data.get('github', None)
        self.__folderIds = []
        for folderId in data.get('folders', []):
            self.__folderIds.append(folderId['resource'].replace(const101.url101explorer, ''))
        self.__fileIds = []
        for fileId in data.get('files', []):
            self.__fileIds.append(fileId['resource'].replace(const101.url101explorer, ''))

        if isinstance(self, Member):
            self.__dict__['_Member__endpoint'] = data['endpoint']
            self.__dict__['_Member__wiki'] = data['wiki']
            self.__dict__['_Member__headline'] = data['headline']

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(Folder, {})'.format(self.__identifier)

    def __eq__(self, other):
        if hasattr(other, 'identifier'):
            return other.identifier == self.identifier
        return NotImplemented


class Member(Folder):
    def __init__(self, identifier, parent=None):
        Folder.__init__(self, identifier, member=self, parent=parent)
        parts = identifier.split('/')

        self.__namespace = wikifyNamespace(parts[0])

        if USE_EXPLORER_SERVICE:
            self.__virtual = None != self.github
        else:
            self.__virtual = not os.path.exists(self.path)
            if not self.name in json.load(open(os.path.join(const101.tRoot, parts[0], 'members.json'), 'r')):
                raise BadIdentifierException(identifier, '{} does not belong to a member')

    @property
    def classifier(self):
        return 'Member'

    @property
    def parent(self):
        if not '_Member__parent' in self.__dict__:
            self.__parent = Namespace(self.identifier.split('/')[0])
        return self.__parent

    @property
    def headline(self):
        if not '_Member__headline' in self.__dict__:
            self.__headline = WikiDump().getHeadline(self.__namespace, self.name)
        return self.__headline

    @property
    def virtual(self):
        return self.__virtual

    @property
    def endpointLink(self, format='json'):
        if not '_Member__endpoint' in self.__dict__:
            self.__endpoint = os.path.join(const101.url101endpoint, self.__namespace + ':' + self.name, format)
        return self.__endpoint

    @property
    def wikiLink(self):
        if not '_Member__wiki' in self.__dict__:
            self.__wiki = os.path.join(const101.url101wiki, self.__namespace + ':' + self.name)
        return self.__wiki

    @property
    def github(self):
        if not '_Member__github' in self.__dict__:
            self.__github = PullRepoDump().getGithubLink(self.name)
        return self.__github

    def __str__(self):
        return '(Member, {})'.format(self.identifier)


#TODO: (File) implement "people" property
class File:
    derivativesTable = helpers.loadDerivativeNames('file')

    def __init__(self, identifier, parent=None, member=None):
        """
        constructor for file class
        :param identifier: identifier for the file (e.g. "constributions/antlrAcceptor/.gitignore)
        :param parent: optional pointer to the parent instance
        :param member: optional pointer to the member instance
        :raise: NonExistingIdentifierException if identifier variable doesn't exist
        """
        self.__identifier = identifier

        if parent:
            self.__parent = parent
        if member:
            self.__member = member

        self.__loadedDerivatives = {}

        if USE_EXPLORER_SERVICE:
            self.__sPath = os.path.join(const101.url101explorer, self.identifier)
            self.__loadFromWeb()
        else:
            self.__sPath = os.path.join(const101.sRoot, identifier)
            self.__tPath = os.path.join(const101.tRoot, identifier)

            if not os.path.isfile(self.__sPath):
                raise BadIdentifierException(identifier)

    @property
    def identifier(self):
        """
        returns the identifier string
        :return: a string representing the identifier
        """
        return self.__identifier

    @property
    def name(self):
        """
        returns the name of this file
        :return: a string representing the filename (only name, not path)
        """
        if not '_File__name' in self.__dict__:
            self.__name = self.identifier.rsplit('/', 1)[1]
        return self.__name

    @property
    def path(self):
        """
        returns the complete path or HTTP url (depending on web/filesystem access)  to this file
        :return: a string representing the path or url
        """
        return self.__sPath

    @property
    def classifier(self):
        return 'File'

    @property
    def member(self):
        """
        returns a backlink to the member this file belongs to
        :return: instance of Member class
        """
        if not '_File__member' in self.__dict__:
            self.__member = Member('/'.join(self.identifier.split('/')[0:2]))
        return self.__member

    @property
    def parent(self):
        """
        returns a backlink to the folder this file belongs to
        :return: instance of folder or member class, depending on where this file is sitting in the file tree
        """
        if not '_File__parent' in self.__dict__:
            pIdentifier = self.identifier.rsplit('/', 1)[0]
            if pIdentifier == self.member.identifier:
                self.__parent = self.member
            else:
                self.__parent = Folder(pIdentifier)

        return self.__parent

    @property
    def fragments(self):
        """
        returns all known fragments this file has
        :return: a list with instances of the Fragment class
        """
        if not '_File__fragments' in self.__dict__:
            self.__fragments = []
            if not '_File__fragmentIds' in self.__dict__:
                self.__fragmentIds = []
                if self.extractor.exists:
                    self.__fragmentIds = [
                        os.path.join(self.__identifier, x['classifier'], x['name']) if 'index' not in x else
                        os.path.join(self.__identifier, x['classifier'], x['name'], x['index'])
                        for x in self.extractor.rawData['fragments']
                    ]
            for id in self.__fragmentIds:
                self.__fragments.append(Fragment(id, member=self.member, file=self, parent=self))

        return self.__fragments

    @property
    def content(self):
        """
        returns the content of the file (if readable, meaning that a geshi code is available)
        :return: a string representing the content
        :raise: NotReadableException if no geshi code is present
        """
        if not '_File__content' in self.__dict__:
            geshi = self.geshi
            if not geshi:
                raise NotReadableException(self.__identifier)
            self.__content = open(self.__sPath, 'r').read()

        return self.__content

    @property
    def geshi(self):
        """
        returns the geshi code for this file (or None)
        :return: a string representing the geshi code or None if there is no code
        """
        if not '_File__geshi' in self.__dict__:
            self.__geshi = None
            matches = self.matches
            if matches.exists:
                self.__geshi = self.matches.select(lambda x: 'geshi' in x)
                #if geshi attribute is found, set it to the actual value instead of the map that might contain a comment
                #if no geshi attribute is found, then the value will already be none
                if self.__geshi:
                    self.__geshi = self.__geshi['geshi']

        return self.__geshi

    @property
    def language(self):
        if not '_File__language' in self.__dict__:
            self.__language = None
            matches = self.matches
            if matches.exists:
                self.__language = self.matches.select(lambda x: 'language' in x)
                if self.__language:
                    self.__language = self.__language['language']

        return self.__language

    @property
    def features(self):
        if not '_File__features' in self.__dict__:
            self.__features = []
            matches = self.matches
            if matches.exists:
                entries = self.matches.filter(lambda x: 'feature' in x)
                for entry in entries:
                    self.__features.append(entry['feature'])
            self.__features = set(self.__features)

        return self.__features

    @property
    def relevance(self):
        if not '_File__relevance' in self.__dict__:
            self.__relevance = 'system'
            matches = self.matches
            if matches.exists:
                relevance = self.matches.select(lambda x: 'relevance' in x)
                if relevance:
                    self.__relevance = relevance['relevance']

        return self.__relevance

    @property
    def isReadable(self):
        """
        returns whether this file is readable or not
        :return: boolean value indicating whether the content property can be used
        """
        return None != self.geshi

    @property
    def derivatives(self):
        """
        returns a list of all derivatives, that (at least in theory) should be there. You must check whether they are
        actually there or not
        :return: a list containing instances of various derivative classes
        """
        for item in File.derivativesTable:
            clssName = File.derivativesTable[item]
            constructor = globals()[clssName]
            if not item in self.__loadedDerivatives:
                self.__loadedDerivatives[item] = constructor(self.identifier)

        return self.__loadedDerivatives.values()

    @property
    def github(self):
        """
        returns the link to this file in a github repository
        :return: a string containing the link to this file in a github repository
        """
        if not '_File__github' in self.__dict__:
            self.__github = self.parent.github + '/' + self.name
        return self.__github

    @property
    def people(self):
        """
        returns a list of all people that are somehow connected to this file
        currently returns an empty list
        :return: a list with instances of the Person class
        """
        return []

    def __loadFromWeb(self):
        data = helpers.loadJSONFromUrl(self.__sPath)

        self.__github = data['github']
        self.__geshi = data['geshi']
        self.__language = data['language']
        if 'content' in data:
            self.__content = data['content']

        self.__fragmentIds = []
        for fragment in data['fragments']:
            self.__fragmentIds.append(fragment['resource'].replace(const101.url101explorer, ''))


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(File, {})'.format(self.__identifier)

    def __eq__(self, other):
        if hasattr(other, 'identifier'):
            return other.identifier == self.identifier
        return NotImplemented

    #private, reflection oriented stuff...
    def __getattr__(self, item):
        if item in self.__loadedDerivatives:
            return self.__loadedDerivatives[item]

        if item in File.derivativesTable:
            clssName = File.derivativesTable[item]
            constructor = globals()[clssName]
            self.__loadedDerivatives[item] = constructor(self.identifier)

            return self.__loadedDerivatives[item]

        raise AttributeError, item


class Fragment:
    def __init__(self, identifier, member=None, file=None, parent=None):
        self.__identifier = identifier

        if member:
            self.__member = member
        if file:
            self.__file = file
        if parent:
            self.__parent = parent

        if USE_EXPLORER_SERVICE:
            self.__loadFromWeb()
        else:
            try:
                self.__fragmentData = self.file.extractor.selectFragment(self.fragmentDescription)
            except:
                raise BadIdentifierException(self.identifier)

    @property
    def identifier(self):
        return self.__identifier

    @property
    def fragmentDescription(self):
        filePart = re.findall('.*\.[^/]*', self.identifier)[0]
        return self.identifier.replace(filePart + '/', '')

    @property
    def name(self):
        if not '_Fragment__name' in self.__dict__:
            splitList = self.identifier.split('/')
            self.__classifier = splitList[-2]
            self.__name = splitList[-1]
            if splitList[-1].isdigit():
                self.__index = splitList[-1]
                self.__name = splitList[-2]
                self.__classifier = splitList[-3]

        return self.__name

    @property
    def classifier(self):
        if not '_Fragment__classifier' in self.__dict__:
            self.name
        return self.__classifier

    @property
    def index(self):
        if not '_Fragment__index' in self.__dict__:
            self.name
        return self.__index

    @property
    def member(self):
        """
        returns a backlink to the member this fragment belongs to
        :return: instance of Member class
        """
        if not '_Fragment__member' in self.__dict__:
            self.__member = Member('/'.join(self.identifier.split('/')[0:2]))
        return self.__member

    @property
    def file(self):
        if not '_Fragment__file' in self.__dict__:
            fIdentifier = re.findall('.*\.[^/]*', self.identifier)[0]
            self.__file = File(fIdentifier)
        return self.__file

    @property
    def parent(self):
        if not '_Fragment__parent' in self.__dict__:
            splitList = self.identifier.split('/')
            pIdentifier = '/'.join(splitList[0:-2])
            if splitList[-1].isdigit():
                pIdentifier = '/'.join(splitList[0:-3])
            if self.member.identifier == pIdentifier:
                self.__parent = self.member
            else:
                if helpers.isFileIdentifier(pIdentifier):
                    self.__parent = File(pIdentifier)
                else:
                    self.__parent = Fragment(pIdentifier)

        return self.__parent

    @property
    def fragments(self):
        if not '_Fragment__fragments' in self.__dict__:
            self.__fragments = []
            if not '_Fragment__fragmentIds' in self.__dict__:
                self.__fragments = [
                    Fragment(os.path.join(self.identifier, x['classifier'], x['name']),
                             member=self.member, file=self.file, parent=self)
                    if 'index' not in x else
                    Fragment(os.path.join(self.identifier, x['classifier'], x['name'], x['index']),
                             member=self.member, file=self.file, parent=self)
                    for x in self.__fragmentData
                ]
            else:
                for id in self.__fragmentIds:
                    self.__fragments.append(Fragment(id, member=self.member, file=self.file, parent=self))

        return self.__fragments

    @property
    def content(self):
        if not '_Fragment__content' in self.__dict__:
            lineFrom, lineTo = self.__lineRange()
            fp = open(self.file.path, 'r')
            txt = [x for i, x in enumerate(fp) if i in range(lineFrom - 1, lineTo)]
            self.__content = ''.join(txt)

        return self.__content

    @property
    def geshi(self):
        return self.file.geshi

    def __lineRange(self):
        fragmentLocator = self.file.matches.select(lambda x: 'locator' in x)
        if fragmentLocator:
            fragmentLocator = os.path.join(const101.sRoot, fragmentLocator['locator'])
            filePath = self.file.path

            cmd = '{} {} < {}'.format(fragmentLocator, self.fragmentDescription, filePath)
            cmd = cmd.replace(';', '\;').replace('|', '\|').replace("'", "\\'")
            status, output = commands.getstatusoutput(cmd)
            if not status == 0:
                raise Exception('fragment locator execution failed')

            data = json.loads(output)
            return data['from'], data['to']

        raise Exception('no fragment locator found (actually, this should\'t be possible)')

    def __loadFromWeb(self):
        data = helpers.loadJSONFromUrl(os.path.join(const101.url101explorer, self.identifier))

        self.__github = data['github']
        self.__geshi = data['geshi']
        if 'content' in data:
            self.__content = data['content']

        self.__fragmentIds = []
        for fragment in data['fragments']:
            self.__fragmentIds.append(fragment['resource'].replace(const101.url101explorer, ''))

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(Fragment, {})'.format(self.__identifier)

    def __eq__(self, other):
        if hasattr(other, 'identifier'):
            return other.identifier == self.identifier
        return NotImplemented


def main():
    #useWebInterface()

    wikidump = WikiDump()
    print wikidump.selectPage('Contribution', 'antlrLexer')

    #languages = Namespace('languages')
    #print languages.name
    #print languages.headline
    #print languages.endpointLink
    #print languages.wikiLink
    #print languages.github
    #print languages.members

    #parent = languages.parent
    #print parent
    #print parent.headline
    #print parent.github

    #help(File.geshi)

    #for page in WikiDump():
    #    print page

    #member = Member('contributions/antlrLexer')
    #print member.name
    #print member.headline
    #print member.endpointLink
    #print member.wikiLink
    #print member.parent

    #f = File('contributions/antlrAcceptor/.gitignore')
    #if f.isReadable:
    #    print 'content:'
    #    print f.content

    #folder = Folder('contributions/antlrLexer/src/test/java/org/softlang/company/tests')
    #file = folder.files[0]
    #print file.member
    #print file.metrics.ncloc
    #print file.fragments
    #print file.language
    #print file.features

if __name__ == '__main__':
    main()



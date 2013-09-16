# 101companies metamodel API
#
# A API that can be used to code against 101companies files
#
#      class    | state
#   ------------+----------
#   Namespace   | unfinished
#   Folder      | unfinished
#   Member      | unfinished
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
def use101Explorer():
    __builtin__.USE_EXPLORER_SERVICE = True


# normal API
class Namespace:
    def __init__(self, identifier):
        parts = identifier.split('/')
        if not parts[0] == 'namespace':
            raise ValueError('Namespace identifiers must have the form "namespace/namespaceName"')

        #ignore namespace/Namespace for now

        self.__identifier = identifier
        self.__name = wikifyNamespace(parts[1])

        #create paths
        self.__sPath = os.path.join(const101.sRoot, dewikifyNamespace(self.__name))
        self.__tPath = os.path.join(const101.tRoot, dewikifyNamespace(self.__name))

    @property
    def name(self):
        return self.__name

    @property
    def classifier(self):
        return 'Namespace'

    @property
    def headline(self):
        if not '_Namespace__headline' in self.__dict__:
            self.__headline = helpers.extractHeadline('Namespace', self.name)
        return self.__headline

    @property
    def wiki(self):
        return const101.url101wiki + 'Namespace/{}'.format(self.name)

    @property
    def github(self):
        raise NotImplementedError('not implemented yet')

    @property
    def endpoint(self):
        raise NotImplementedError('not implemented yet')

    @property
    def sesame(self):
        raise NotImplementedError('do we really need this?')

    @property
    def members(self):
        if not '_Namespace__members' in self.__dict__:
            path = os.path.join(self.__tPath, 'members.json')
            self.__members = [Member(os.path.join(dewikifyNamespace(self.__name), x)) for x in json.load(open(path, 'r'))]
        return self.__members

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(Namespace, {})'.format(self.name)


class Folder:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__name = identifier.rsplit("/", 1)[1]

        #create paths
        self._sPath = os.path.join(const101.sRoot, identifier)
        self._tPath = os.path.join(const101.tRoot, identifier)

        if not isinstance(self, Member):
            if not os.path.exists(self._sPath):
                raise ValueError('Identifier does not exist')

    @property
    def identifier(self):
        return self.__identifier

    @property
    def name(self):
        return self.__name

    @property
    def classifier(self):
        return 'Folder'

    @property
    def folders(self):
        if not '_Folder__folders' in self.__dict__:
            self.__folders = []
            if not hasattr(self, 'virtual') or not self.virtual:
                self.__folders = [Folder(os.path.join(self.__identifier, o)) for o in os.listdir(self._sPath)
                                  if os.path.isdir(os.path.join(self._sPath, o))]

        return self.__folders

    @property
    def files(self):
        if not '_Folder__files' in self.__dict__:
            self.__files = []
            if not hasattr(self, 'virtual') or not self.virtual:
                self.__files = [File(os.path.join(self.__identifier, o)) for o in os.listdir(self._sPath)
                                if os.path.isfile(os.path.join(self._sPath, o))]

        return self.__files

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '(Folder, {})'.format(self.name)

#    def __getattr__(self, item):
#        raise AttributeError, item


class Member(Folder):
    def __init__(self, identifier):
        Folder.__init__(self, identifier)
        self.__namespace = wikifyNamespace(identifier.split('/', 1)[0])

        self.__virtual = not os.path.exists(self._sPath)

        if not self.name in json.load(open(os.path.join(const101.tRoot, identifier.rsplit('/',1)[0], 'members.json'), 'r')):
            raise ValueError('Identifier does not belong to a member')

    @property
    def classifier(self):
        return 'Member'

    @property
    def namespace(self):
        return self.__namespace

    @property
    def headline(self):
        if not '_Member__headline' in self.__dict__:
            self.__headline = helpers.extractHeadline(self.namespace, self.name)
        return self.__headline

    @property
    def virtual(self):
        return self.__virtual

    @property
    def endpoint(self):
        raise NotImplementedError('not implemented yet')

    @property
    def sesame(self):
        raise NotImplementedError('do we really need this?')

    @property
    def wiki(self):
        raise NotImplementedError('not yet implemented')

    @property
    def github(self):
        if not '_Member__github' in self.__dict__:
            self.__github = PullRepoDump().getGithubLink(self.name)
        return self.__github

    def __str__(self):
        return '(Member, {})'.format(self.name)


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
            self.__loadFromExplorer()
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
            pIdentifier = self.identifier.rsplit('/',1)[0]
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

    def __loadFromExplorer(self):
        data = helpers.loadJSONFromUrl(self.__sPath)

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
        return self.identifier.replace(filePart+'/', '')

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


        #if not '_File__fragments' in self.__dict__:
        #self.__fragments = []
        #if not '_File__fragmentIds' in self.__dict__:
        #    self.__fragmentIds = []
        #    if self.extractor.exists:
        #        self.__fragmentIds = [
        #            os.path.join(self.__identifier, x['classifier'], x['name']) if 'index' not in x else
        #            os.path.join(self.__identifier, x['classifier'], x['name'], x['index'])
        #            for x in self.extractor.rawData['fragments']
        #        ]
        #for id in self.__fragmentIds:
        #    self.__fragments.append(Fragment(id))

        #return self.__fragments

    @property
    def content(self):
        if not '_Fragment__content' in self.__dict__:
            lineFrom, lineTo = self.__lineRange()
            fp = open(self.file.path, 'r')
            txt = [x for i, x in enumerate(fp) if i in range(lineFrom-1, lineTo)]
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

        raise Exception('no fragment locator found (actually, this should\'t be possible')

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


if __name__ == '__main__':
    #use101Explorer()

    f = File('contributions/antlrAcceptor/.gitignore')
    if f.isReadable:
        print 'content:'
        print f.content

    print "parent name {}".format(f.parent.name)
    print f.member

    print f.derivatives
    print f.github


    #ns = Namespace(identifier='namespace/languages')
    #print ns
    #print ns.headline
    #print ns.members

    #for m in ns.members:
    #   if m.name == 'Java':
    #       print m.namespace
    #       print m.headline
    #       print m.folders
    #       print m.files

    #folder = Folder('contributions/antlrLexer/src/test/java/org/softlang')
    #print folder.folders

    file = File('contributions/aspectJ/org/softlang/features/Operations.java')
    print file.geshi
    print file.content

    fragment = file.fragments[0]
    print fragment.name
    print fragment.classifier
    print fragment.geshi

    #print fragment.parent
    #print fragment.file
    #print fragment.member
    print fragment.content





# this was the first prototype of the idea:
# def _parse101MetaType(fromFile, info):
#     properties = info['properties']
#     result = {}
#     for entry in fromFile:
#         metadata = entry['metadata']
#         if not isinstance(metadata, types.ListType):
#             metadata = [metadata]
#
#         for m in metadata:
#             for key in m.keys():
#                 if key in properties:
#                     if properties[key].get('multiple', False):
#                         if not key in result:
#                             result[key] = []
#                         if m[key] not in result[key]:
#                             result[key].append(m[key])
#                     else:
#                         result[key] = m[key]
#     return result
#
#
# def _parseSimple(fromFile, info):
#     properties = info['properties']
#     result = {}
#     for key in fromFile.keys():
#         if key in properties:
#             result[key] = fromFile[key]
#
#     return result
#
# def _parseMapToProperty(fromFile, info):
#     result = {}
#     for key in info['properties'].keys():
#         result[key] = fromFile
#
#     return result
#
#
# metadata = {
#     '.matches.json': {
#         'type' : '101meta',
#         'properties': {
#             'relevance': {
#                 'default': 'system',
#             },
#             'language': {
#             }
#         }
#     },
#     '.predicates.json': {
#         'type': '101meta',
#         'properties': {
#             'dependsOn': {
#                 'multiple': True
#             }
#         }
#     },
#     '.metrics.json': {
#         'type': 'simple',
#         'properties': {
#             'size' : {},
#             'ncloc': {},
#             'loc'  : {}
#         }
#     },
#     '.refinedTokens.json': {
#         'type': 'mapToProperty',
#         'properties': {
#             'tokens': {}
#         }
#     }
# }
#
# parsing = {
#     '101meta': _parse101MetaType,
#     'simple' : _parseSimple,
#     'mapToProperty': _parseMapToProperty
# }
#
#
# class Entity:
#     def __init__(self, identifier):
#         if identifier.endswith('/'):
#             identifier = identifier[:-1]
#         if identifier.startswith('/'):
#             identifier = identifier[1:]
#
#         self.identifier = identifier
#         self.name = identifier.split('/')[-1]
#
#     def __str__(self):
#         return json.dumps(self.__dict__)
#
#     def __repr__(self):
#         return self.__str__()
#
#     def _loadMetadataFile(self, extension):
#         global metadata
#         global parsing
#         properties = metadata[extension]['properties']
#
#         #setting default values
#         for propName in properties:
#             if 'multiple' in properties[propName]:
#                 self.__dict__[propName] = []
#             if 'default' in properties[propName]:
#                 self.__dict__[propName] = properties[propName]['default']
#
#         #loading file, calling parsing method
#         filePath = os.path.join(const101.tRoot, self.identifier + extension)
#         fromFile = json.load(open(filePath))
#
#         self.__dict__.update(parsing[metadata[extension]['type']](fromFile, metadata[extension]))
#
#     def __getattr__(self, item):
#         global metadata
#         for ext in metadata.keys():
#             for property in metadata[ext]['properties']:
#                 if property == item:
#                     if not ext in self._loaded:
#                         self._loaded.append(ext)
#                         self._loadMetadataFile(ext)
#
#         if not item in self.__dict__:
#             raise AttributeError(self.__class__.__name__ + ' has no attribute ' + item)
#
#         return self.__dict__.get(item, None)
#
#
# class Folder(Entity):
#     def __init__(self, identifier):
#         Entity.__init__(self, identifier)
#         self.classifier = 'Folder'
#
#     @property
#     def Files(self):
#         files = []
#         filePath = os.path.join(const101.sRoot, self.identifier)
#         for file in os.listdir(filePath):
#             path = os.path.join(self.identifier, file)
#             if os.path.isfile(os.path.join(const101.sRoot, path)):
#                 files.append( File(path) )
#
#         return files
#
#     @property
#     def Folders(self):
#         folders = []
#         filePath = os.path.join(const101.sRoot, self.identifier)
#         for folder in os.listdir(filePath):
#             path = os.path.join(self.identifier, folder)
#             if os.path.isfile(os.path.join(const101.sRoot, path)):
#                 folders.append( Folder(path) )
#
#         return folders
#
#
# class File(Entity):
#     def __init__(self, identifier):
#         Entity.__init__(self, identifier)
#         self.classifier = 'File'
#         self._loaded = []
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# if __name__ == '__main__':
#     folder = Folder('contributions/antlrLexer/src/test/java/org/softlang/tests')
#     for file in folder.Files:
#         print file.name
#         print '------------'
#         print file.language
#         print file.relevance
#         print file.size
#         print file.tokens
#         print file.dependsOn
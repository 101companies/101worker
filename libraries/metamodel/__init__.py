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
from connection import Connection

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
        """
        constructor for the Namespace class
        @param identifier: the identifier for the namespace, e.g. namespace/contributions
        @type identifier: str
        @param parent: optional parameter indicating the parent - don't use if you're instantiating the class yourself
        @type parent Namespace
        @return: an instance of this class
        @rtype: Namespace
        """
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
        """
        describes the unique identifier for this namespace
        @return: the identifier as a string
        @rtype: str
        """
        return self.__identifier

    @property
    def name(self):
        """
        describes the wikified name of this namespace (e.g. "Contribution")
        @return: the name as a string
        @rtype: str
        """
        if not '_Namespace__name' in self.__dict__:
            self.__name = wikifyNamespace(self.identifier)
        return self.__name

    @property
    def path(self):
        """
        describes the path on the 101worker filesystem for this namespace
        @return: the path as a string
        @rtype: str
        """
        return self.__sPath

    @property
    def classifier(self):
        """
        the classifier of this namespace (obviously, it's "Namespace")
        @return: the classifier as a string
        @rtype: str
        """
        return 'Namespace'

    @property
    def parent(self):
        """
        describes the parent of this namespace. If the namespace is already the highest one, "None" will be returned
        @return: an instance of namespace or None
        @rtype: str
        """
        if not '_Namespace__parent' in self.__dict__:
            if self.identifier == 'namespaces':
                self.__parent = None
            else:
                self.__parent = Namespace('namespaces')
        return self.__parent

    @property
    def headline(self):
        """
        query for the headline of the wiki page associated with this namespace. The markup will already be removed.
        @return: the headline as a string
        @rtype: str
        """
        if not '_Namespace__headline' in self.__dict__:
            self.__headline = WikiDump().getHeadline('Namespace', self.name)
        return self.__headline

    @property
    def endpointLink(self, format='json'):
        """
        describes the link to the endpoint that can be used to access the wiki triples for this namespace
        @param: format: the format of the triples
        @type format str
        @return: the link as a string
        @rtype: str
        @warning: The format is currently fixed at JSON
        """
        if not '_Namespace__endpoint' in self.__dict__:
            self.__endpoint = os.path.join(const101.url101endpoint, 'Namespace:' + self.name, format)
        return self.__endpoint

    @property
    def wikiLink(self):
        """
        describes the link to the wiki page (the actual page - not the API page)
        @return: the link as a string
        @rtype: str
        """
        if not '_Namespace__wiki' in self.__dict__:
            self.__wiki = os.path.join(const101.url101wiki, 'Namespace' + ':' + self.name)
        return self.__wiki

    @property
    def github(self):
        """
        describes the link to the github page for this namespace
        @return: the link as a string
        @rtype: str
        """
        if not '_Namespace__github' in self.__dict__:
            relPath = self.identifier
            if self.identifier == 'namespaces':
                relPath = ''
            self.__github = os.path.join(const101.url101repo, relPath)
        return self.__github

    @property
    def members(self):
        """
        returns the members of this namespace. This can either be a list of other Namespaces or a list of Member
        instances.
        @return: a list containing Member of Namespace instances
        @rtype: list Member or Namespace
        """
        if not '_Namespace__members' in self.__dict__:
            self.__members = []
            if not '_Namespace__memberIds' in self.__dict__:
                self.__memberIds = [os.path.join(self.identifier, mId) for mId in
                                    json.load(open(os.path.join(self.__tPath, 'members.json')))]
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
        """
        Constructor for the Folder class.
        @param identifier:
        @type identifier str
        @param member:  optional parameter to set the member of this folder (leave out if you're instancing this class
        directly)
        @type member Member
        @param parent: optional parameter to set the parent of this folder (leave out if you're instancing this class
        directly)
        @type parent Folder
        @return: a instance of the Folder class
        @rtype: Folder
        """
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
        """
        The identifier for this folder.
        @return: the identifier
        @rtype str
        """
        return self.__identifier

    @property
    def name(self):
        """
        The name of this folder.
        @return: the name
        @rtype str
        """
        return self.__name

    @property
    def path(self):
        """
        The path to this folder on 101worker relative to modules directory of 101worker.
        @return: the relative path
        @rtype str
        """
        return self.__sPath

    @property
    def classifier(self):
        """
        The classifier of this folder (obviously "Folder").
        @return: the classifier
        @rtype str
        @deprecated Marked for deletion - ask instead for name of the class (e.g. x.__class__.__name__)
        """
        return 'Folder'

    @property
    def member(self):
        """
        Returns a backlink to the member this file belongs to.
        @return: the Member this folder belongs to
        @rtype Member
        """
        if not '_Folder__member' in self.__dict__:
            self.__member = Member('/'.join(self.identifier.split('/')[0:2]))
        return self.__member

    @property
    def parent(self):
        """
        Returns the parent of this folder, which is either a Member of another folder depending on where this folder is
        in the filesystem tree. This is usually no problem, since a Member is only a special Folder and therefore
        derived from it.
        @return: the parent (Member or Folder instance)
        @rtype Folder or Member
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
        """
        Returns a list of sub-folders, that this folder contains.
        @return: a list of Folder instances
        @rtype list of Folder
        """
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
        """
        Returns a list of files that this folder contains.
        @return: a list of file instances
        @rtype list of File
        """
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
        """
        Returns a list of derived resources that exist for this Folder.
        @return: a list of Derivative instances
        @rtype list
        @warning As no important derived resources for folders exist at the moment, this method will always return an
        empty list.
        """
        return []

    @property
    def github(self):
        """
        Returns the link to the Github repository that contains this folder.
        @return: the link as a string
        @rtype str
        """
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
        """
        The Constructor for the Member class.
        @param identifier: the unique identifier for the member (e.g."contributions/antlrLexer")
        @type identifier str
        @param parent: optional parameter to set the parent of this member (leave out if you're instancing this class
        directly)
        @type parent Namespace
        @return: a instance of Member
        @rtype Member
        """
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
        """
        The classifier of this member (obviously "Member").
        @return: the classifier
        @rtype str
        @deprecated Marked for deletion - ask instead for name of the class (e.g. x.__class__.__name__)
        """
        return 'Member'

    @property
    def parent(self):
        """
        The parent of this member, which is a namespace.
        @return: the parent namespace
        @rtype Namespace
        """
        if not '_Member__parent' in self.__dict__:
            self.__parent = Namespace(self.identifier.split('/')[0])
        return self.__parent

    @property
    def headline(self):
        """
        Queries for the headline of the wiki page that is associated with this member. The returned string will already
        be removed of markup.
        @return: the headline
        @rtype str
        """
        if not '_Member__headline' in self.__dict__:
            self.__headline = WikiDump().getHeadline(self.__namespace, self.name)
        return self.__headline

    @property
    def virtual(self):
        """
        Returns whether this member physically exists on the 101worker filesystem or not.
        @return: a bool indicating physical existence
        @rtype bool
        """
        return self.__virtual

    @property
    def endpointLink(self, format='json'):
        """
        Describes the link to the endpoint that can be used to access the wiki triples for this member.
        @param: format: the format of the triples
        @type format str
        @return: the link as a string
        @rtype: str
        @warning: The format is currently fixed at JSON
        """
        if not '_Member__endpoint' in self.__dict__:
            self.__endpoint = os.path.join(const101.url101endpoint, self.__namespace + ':' + self.name, format)
        return self.__endpoint

    @property
    def endpointData(self):
        """
        Queries the endpoint for the actual wiki triples that exist for this member.
        @return: a list of string triples [ [s1, p1, o1], ... ]
        @rtype list
        """
        if not '_Member__endpointData' in self.__dict__:
            self.__endpointData = helpers.loadJSONFromUrl(self.endpointLink)
        return self.__endpointData

    @property
    def wikiLink(self):
        """
        Describes the link to the actual wiki page (not the API link!).
        @return: the link as a string
        @rtype str
        """
        if not '_Member__wiki' in self.__dict__:
            self.__wiki = os.path.join(const101.url101wiki, self.__namespace + ':' + self.name)
        return self.__wiki

    @property
    def implements(self):
        """
        Inspects the wiki triples for "implements" links and returns them with their namespace removed.
        @return: the list of features
        @rtype list of str
        """
        if not '_Member__implements' in self.__dict__:
            self.__implements = []

            connection = Connection('http://triples.101companies.org/openrdf-sesame/')
            connection.use_repository('Testing_2')

            connection.addnamespace('onto', 'http://101companies.org/ontology#')
            connection.addnamespace('res', 'http://101companies.org/resources#')
            res = connection.query('SELECT DISTINCT ?feature WHERE { <http://101companies.org/resources#'+self.name+'> <http://101companies.org/ontology#implements> ?feature }')
            for feature in res:
                val = feature['feature']['value'].replace('http://101companies.org/resources#','').replace('_',' ')
                self.__implements.append(val)

        return self.__implements

    @property
    def github(self):
        """
        Returns the link to the Github repository this member is contained in.
        @return: the link as a string
        @rtype str
        """
        if not '_Member__github' in self.__dict__:
            self.__github = PullRepoDump().getGithubLink(self.name)
        return self.__github

    def __str__(self):
        return '(Member, {})'.format(self.identifier)


class File:
    derivativesTable = helpers.loadDerivativeNames('file')

    def __init__(self, identifier, parent=None, member=None):
        """
        The Constructor for the File class.
        @param identifier: the unique identifier for the member (e.g."contributions/antlrAcceptor/.gitignore")
        @type identifier str
        @param parent: optional parameter to set the parent of this file (leave out if you're instancing this class
        directly)
        @type parent Folder
        @param member: optional parameter to set the member of this file (leave out if you're instancing this class
        directly)
        @type member Member
        @return: a instance of File
        @rtype File
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
        The identifier for this file.
        @return the identifier as a string
        @rtype str
        """
        return self.__identifier

    @property
    def name(self):
        """
        The name of this file.
        @return the name as a string
        @rtype str
        """
        if not '_File__name' in self.__dict__:
            self.__name = self.identifier.rsplit('/', 1)[1]
        return self.__name

    @property
    def path(self):
        """
        The path for this file relative to the directory of a module.
        @return: The relative path as a string
        @rtype str
        """
        return self.__sPath

    @property
    def classifier(self):
        """
        The classifier of this file (obviously "File").
        @return: the classifier
        @rtype str
        @deprecated Marked for deletion - ask instead for name of the class (e.g. x.__class__.__name__)
        """
        return 'File'

    @property
    def member(self):
        """
        Returns the member of this file.
        @return: the parent (Member instance)
        @rtype Member
        """
        if not '_File__member' in self.__dict__:
            self.__member = Member('/'.join(self.identifier.split('/')[0:2]))
        return self.__member

    @property
    def parent(self):
        """
        Returns the parent of this file, which is either a Member of another folder depending on where this folder is
        in the filesystem tree. This is usually no problem, since a Member is only a special Folder and therefore
        derived from it.
        @return: the parent (Member or Folder instance)
        @rtype Folder or Member
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
        Queries for fragments that are contained in this files based on .extractor.json files
        @return: a list of Fragment instances
        @rtype list of Fragment
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
        Returns the content of the file, if the file is readable. Readability is dependent on the presence of
        a geshi code. If no code is available for this file, it is deemed unreadable.
        @return: the content as a string
        @rtype str
        @raise NotReadableException if the file is considered unreadable
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
        Returns the geshi code for this file as queried through .matches.json files.
        @return: the geshi code as a string or None
        @rtype str or None
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
        """
        Returns the language of this file as queried through .matches.json files.
        @return: the language as a string or None
        @rtype str or None
        """
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
        """
        Returns a list of features for this file as queried through .matches.json or .predicates.json files.
        @return: a list of features (represented as strings)
        @rtype list of str
        """
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
    def dependsOn(self):
        """
        Returns the technologies, this file depends on as queried through .matches.json or .predicates.json files.
        @return: a list of technologies (represented as strings)
        @rtype: list of str
        """
        if not '_File__dependsOn' in self.__dict__:
            self.__dependsOn = []
            matches = self.matches
            if matches.exists:
                entries = self.matches.filter(lambda x: 'dependsOn' in x)
                for entry in entries:
                    self.__dependsOn.append(entry['dependsOn'])

        return self.__dependsOn

    @property
    def relevance(self):
        """
        Returns the relevance of the file as queried through .matches.json or .predicate.json files. If no info is
        available, this file is considered to be system code. Relevance values are: ["system", "derive", "reuse",
        "test", "ignore"]
        @return: the relevance as a string
        @rtype str
        """
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
        Returns whether this file is readable or not.
        @return: a bool indicating readability
        @rtype bool
        """
        return None != self.geshi

    @property
    def derivatives(self):
        """
        Returns a list of all derived files, that possibly exist for this file. Whether the derivative does really
        exist has to be asked for each derivative individually.
        @return: a list of concrete Derivative-subclasses instances
        @rtype list of Derivative
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
        Returns the list to the Github repository that contains this file (direct link to file).
        @return: the link as a string
        @rtype str
        """
        if not '_File__github' in self.__dict__:
            self.__github = self.parent.github + '/' + self.name
        return self.__github

    @property
    def people(self):
        """
        Returns a list of all people associated with this file.
        @return: a list
        @rtype list
        @warning will currently always return an empty list, as no real information is avaible at the moment
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
        """
        The constructor for the Fragment class.
        @param identifier: The unique identifier for the fragment - usually a file identifier plus a fragment
        description.
        @type identifier str
        @param parent: optional parameter to set the parent of this fragment (leave out if you're instancing this class
        directly)
        @type parent File or Fragment
        @param file: optional parameter to set the file of this fragment (leave out if you're instancing this class
        directly)
        @type file File
        @param member: optional parameter to set the member of this fragment (leave out if you're instancing this class
        directly)
        @type member Member
        @return: a instance of the Fragment class
        @rtype Fragment
        """
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
        """
        Returns the identifier for this fragment.
        @return: the identifier as a string
        @rtype str
        """
        return self.__identifier

    @property
    def fragment_description(self):
        """
        Returns the fragment description of this fragment. This is the complete identfier minus the identifier for the
        file.
        @return: the fragment description as a string
        @rtype str
        """
        filePart = re.findall('.*\.[^/]*', self.identifier)[0]
        return self.identifier.replace(filePart + '/', '')

    @property
    def name(self):
        """
        Returns the name of the fragment.
        @return: the name as a string
        @rtype str
        """
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
        """
        Returns the classifier of the fragment ("method", "class", ...). Classifier are language specific!
        @return: the classifier as a string
        @rtype str
        """
        if not '_Fragment__classifier' in self.__dict__:
            self.name
        return self.__classifier

    @property
    def index(self):
        """
        Returns the index
        @return: the index as a int
        @rtype int
        @warning not implemented yet - will always return 0
        """
        #TODO: Fix me!
        if not '_Fragment__index' in self.__dict__:
            self.__index = 0
        return self.__index

    @property
    def member(self):
        """
        Returns the backlink to the member this fragment belongs to.
        @return: the Member instance this fragment belongs to
        @rtype Member
        """
        if not '_Fragment__member' in self.__dict__:
            self.__member = Member('/'.join(self.identifier.split('/')[0:2]))
        return self.__member

    @property
    def file(self):
        """
        Returns the backlink to the file this fragment belongs to.
        @return: the File instance this fragment is contained in
        @rtype File
        """
        if not '_Fragment__file' in self.__dict__:
            fIdentifier = re.findall('.*\.[^/]*', self.identifier)[0]
            self.__file = File(fIdentifier)
        return self.__file

    @property
    def parent(self):
        """
        Returns the parent of this fragment. This can either be another fragment or a file.
        @return: the parent (either Fragment or File)
        @rtype Fragment or File
        """
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
        """
        Returns the sub-fragments contained in this fragment as a list.
        @return: a list of Fragment instances
        @rtype list of Fragment
        """
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
        """
        Returns the content of the fragment. This is dependent on the existence of a fragment locator for this
        type of file.
        @return: the content as a string
        @rtype str
        """
        if not '_Fragment__content' in self.__dict__:
            lineFrom, lineTo = self.__line_range()
            fp = open(self.file.path, 'r')
            txt = [x for i, x in enumerate(fp) if i in range(lineFrom - 1, lineTo)]
            self.__content = ''.join(txt)

        return self.__content

    @property
    def geshi(self):
        """
        Returns the geshi code for this fragment (actually, it asks the file for the geshi code).
        @return: the geshi code as a string
        @rtype str
        """
        return self.file.geshi

    def __line_range(self):
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

    #wikidump = WikiDump()
    #print wikidump.selectPage('Contribution', 'antlrLexer')

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

    member = Member('contributions/antlrLexer')
    print member.name
    print member.headline
    print member.endpointLink
    print member.wikiLink
    print member.parent
    print member.implements

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



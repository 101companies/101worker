import json
import sys
import os
import types
import wikiFunctions

sys.path.append('../101meta')
sys.path.append('..')
import const101

from mediawiki import wikifyNamespace
from mediawiki import dewikifyNamespace


class NonExistingIdentifierException(Exception):
    def __init__(self, identifier):
        self.value = 'Identifier {} does not exist'.format(identifier)

    def __str__(self):
        return repr(self.value)


class NonExistingPathException(Exception):
    def __init__(self, path):
        self.value = 'Path {} does not exist'.format(path)

    def __str__(self):
        return repr(self.value)


class NotReadableException(Exception):
    def __init__(self, path):
        self.value = "Can't read content from {}, because there is no geshi code assigned".format(path)


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
            self.__headline = wikiFunctions.extractHeadline('Namespace', self.name)
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
        return 'Namespace: {}'.format(self.name)


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
    def github(self):
        raise NotImplementedError('not yet implemented')

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
        return 'Folder: {}'.format(self.name)

    def __getattr__(self, item):
        print 'just a test'
        raise AttributeError, item


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
            self.__headline = wikiFunctions.extractHeadline(self.namespace, self.name)
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

    def __str__(self):
        return 'Member : {}'.format(self.name)


class File:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__loadedDerivatives = {}

        self.__sPath = os.path.join(const101.sRoot, identifier)
        self.__tPath = os.path.join(const101.tRoot, identifier)

        if not os.path.isfile(self.__sPath):
            raise NonExistingIdentifierException(identifier)

    @property
    def identifier(self):
        return self.__identifier

    @property
    def fragments(self):
        if not '_File__fragments' in self.__dict__:
            self.__fragments = [
                Fragment(os.path.join(self.__identifier, x['classifier'], x['name'])) if 'index' not in x else
                Fragment(os.path.join(self.__identifier, x['classifier'], x['name'], x['index']))
                for x in self.extractor.rawData['fragments']
            ]
        return self.__fragments

    @property
    def derivatives(self):
        raise NotImplementedError('not yet implemented')

    @property
    def content(self):
        if not '_File__content' in self.__dict__:
            geshi = self.geshi
            if not geshi:
                raise NotReadableException(self.__identifier)
            self.__content = open(self.__sPath, 'r').read()

        return self.__content

    @property
    def geshi(self):
        if not '_File__geshi' in self.__dict__:
            self.__geshi = None
            matches = self.matches
            if matches:
                self.__geshi = self.matches.select(lambda x: 'geshi' in x)
                #if geshi attribute is found, set it to the actual value instead of the map that might contain a comment
                if self.__geshi:
                    self.__geshi = self.__geshi['geshi']

        return self.__geshi

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'File : {}'.format(self.__identifier)

    def __loadDerived(self, clss):
        try:
            return clss(self.identifier)
        except NonExistingPathException:
            return None

    def __getattr__(self, item):
        if item not in self.__loadedDerivatives and item == 'matches':
            self.__loadedDerivatives['matches'] = self.__loadDerived(Matches)

        if item not in self.__loadedDerivatives and item == 'extractor':
            self.__loadedDerivatives['extractor'] = self.__loadDerived(Extractor)

        if item in self.__loadedDerivatives:
            return self.__loadedDerivatives[item]

        raise AttributeError, item


class Fragment:
    def __init__(self, identifier):
        self.__identifier = identifier
        pass

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.__identifier


#abstract class
class Derivative:
    def __init__(self, path):
        if self.__class__.__name__ == 'Derivative':
            raise NotImplementedError('This class is abstract')

        if not os.path.exists(path):
            raise NonExistingPathException(path)

        self.__path = path

    @property
    def rawData(self):
        if not '_Derivative__raw_data' in self.__dict__:
            if os.path.exists(self.path):
                self.__raw_data = json.load(open(self.path, 'r'))

        return self.__raw_data

    @property
    def path(self):
        return self.__path


class Metrics(Derivative):
    def __init__(self):
        pass


class Meta101(Derivative):
    def select(self, filterFunc):
        for entry in self.rawData:
            entry = entry['metadata']
            if not isinstance(entry, types.ListType):
                entry = [entry]
            for e in entry:
                if filterFunc(e):
                    return e


class Matches(Meta101):
    def __init__(self, identifier):
        p = os.path.join(const101.tRoot, identifier + '.matches.json')
        Derivative.__init__(self, p)


class Extractor(Derivative):
    def __init__(self, identifier):
        p = os.path.join(const101.tRoot, identifier+'.extractor.json')
        Derivative.__init__(self, p)


if __name__ == '__main__':
    f = File('contributions/antlrAcceptor/.gitignore')
    try:
        f.content
    except NotReadableException:
        print 'works as expected'

    ns = Namespace(identifier='namespace/languages')
    print ns
    print ns.headline
    print ns.members

    for m in ns.members:
       if m.name == 'Java':
           print m.namespace
           print m.headline
           print m.folders
           print m.files

    folder = Folder('contributions/antlrLexer/src/test/java/org/softlang')
    print folder.folders

    file = File('contributions/antlrLexer/src/test/java/org/softlang/tests/Parsing.java')
    print file.geshi
    print file.geshi
    print file.content
    print file.fragments






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
#! /usr/bin/env python
from rdflib.term import URIRef

__author__ = 'Martin Leinberger'

from helpers.Namespaces import rdf, rdfs, ontology, nameSpaceByName
from helpers.Errorlog import reportError


class Property:
    Properties = {}
    SubProperties = {}

    def __init__(self, domain, description):
        self.name = description['property']
        Property.Properties[self.name] = self

        self.subPropertyOf = description.get('super', None)
        if self.subPropertyOf:
            self.SubProperties.setdefault(self.subPropertyOf, []).append(self)
        self.range = description['range']
        self.domain = domain

    # I dislike this name
    def transitiveProperty(self):
        if self.subPropertyOf: return [ self ] + Property.Properties[self.subPropertyOf].transitiveProperty()
        else: return [ self ]

    def toRDF(self):
        triples = [
            (ontology[self.name], rdf['type'], rdfs['Property']),
            (ontology[self.name], rdfs['domain'], ontology[self.domain]),
            (ontology[self.name], rdfs['range'], ontology[self.range])
        ]
        if self.subPropertyOf: triples += [(ontology[self.name], rdfs['subPropertyOf'], ontology[self.subPropertyOf])]
        return triples

    def toPredicate(self, domain, range):
        if not domain or not range:
            return ontology[self.name]
        for sub in self.SubProperties.get(self.name, []):
            if self.name == 'implements':
                if sub.domain == domain and sub.range == range:
                    return sub.toPredicate(None,None)
        return ontology[self.name]

    def __eq__(self, other):
        if hasattr(other, 'name'):
            return other.name == self.name
        if isinstance(other, basestring):
            return other == self.name
        return False

    def __ne__(self, other):
        if hasattr(other, 'name'):
            return other.name != self.name
        if isinstance(other, basestring):
            return other != self.name
        return True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self): return self.name.__hash__()


class MappingProperty:
    def __init__(self, description):
        self.name = description['property']
        Property.Properties[self.name] = self

        x = description['mapsTo']
        if not ':' in x: self.ns, self.afterMappingName = 'ontology', description['mapsTo']
        else: self.ns, self.afterMappingName = description['mapsTo'].split(':')

    def transitiveProperty(self):
        return [ self ]

    def toRDF(self): return []

    def toPredicate(self, domain, range):
        return nameSpaceByName(self.ns)[self.afterMappingName]


    def __eq__(self, other):
        if hasattr(other, 'name'):
            return other.name == self.name
        if isinstance(other, basestring):
            return other == self.name
        return False

    def __ne__(self, other):
        if hasattr(other, 'name'):
            return other.name != self.name
        if isinstance(other, basestring):
            return other != self.name
        return True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()

    def __hash__(self): return self.name.__hash__()


class ConceptModel:
    Models = {}

    def __init__(self, description):
        self.id = description['@id']
        ConceptModel.Models[self.id] = self

        self.subClassOf = description.get('@type', [])
        if not isinstance(self.subClassOf, list): self.subClassOf = [ self.subClassOf ]
        self.defined_properties = \
            [Property(self.id, x) for x in description.get('properties',[])] \
            + [MappingProperty(x) for x in description.get('mapping', [])]

    def Types(self):
        x = [self.id]
        for superClass in self.subClassOf:
            x += ConceptModel.Models[superClass].Types()
        return x

    def Properties(self):
        x = self.defined_properties
        for superClass in self.subClassOf:
            if superClass in ConceptModel.Models:
                x += ConceptModel.Models[superClass].Properties()
        return [j for i in map(lambda x: x.transitiveProperty(), x) for j in i]

    def toRDF(self):
        return [ (ontology[self.id], rdf['type'], rdfs['Class']) ] \
        + [(ontology[self.id], rdfs['subClassOf'], ontology[x]) for x in self.subClassOf]


class WikiResource:
    def __init__(self, description):
        self.ns = description['p']
        if not self.ns: self.ns = 'Concept'
        #assert not self.ns is None
        self.name = description['n']
        self.jsonDescription = description

    def toRDF(self):
        entity = nameSpaceByName(self.ns)[self.name]
        model = ConceptModel.Models[self.ns]
        triples = []
        allowedProperties = set(model.Properties())
        for property in self.jsonDescription:
            if property in allowedProperties:
                for object in self.jsonDescription[property]:
                    try:
                        if isinstance(object, dict):
                            if not object['p']:
                                # Its a special case if the relation is a instance relation
                                if property == 'instanceOf': object['p'] = 'Ontology'
                                else: object['p'] = 'Concept'
                            triples.append( (entity, Property.Properties[property].toPredicate(self.ns, object['p']),
                                             nameSpaceByName(object['p'])[object['n']]) )

                        elif isinstance(object, basestring):
                            object = URIRef(object)
                            triples.append( (entity, Property.Properties[property].toPredicate(None, None), object) )
                    except: pass
            else:
                if property not in ['headline', 'p', 'n', 'internal_links', 'subresources', 'isA']:
                    reportError(self.jsonDescription, 'Undefined property: {}'.format(property))

        return triples


class WikiConcept:
    def __init__(self, description):
        self.ns = 'Ontology'
        self.name = description['n']
        self.jsonDescription = description

    def toRDF(self):
        clss = nameSpaceByName(self.ns)[self.name]
        entity = nameSpaceByName('Concept')[self.name]
        triples = []
        for c in self.jsonDescription['isA']:
            triples.append( (clss, rdfs['subClassOf'], nameSpaceByName('Ontology')[c['n']]) )

        triples.append( (entity, rdf['type'], clss) )
        triples.append( (clss, ontology['classifies'], entity) )

        #for property in self.jsonDescription:
            #Ignored as specific to the concept
        #    if property not in ['isA']:
        #        if property in ['memberOf', 'mentions']:
        #            for object in self.jsonDescription[property]:
        #                if isinstance(object, dict):
        #                    if not object['p']: object['p'] = 'Concept'
        #                    #print 'object: {}'.format(object)
        #                    object = nameSpaceByName(object['p'])[object['n']]
        #                elif isinstance(object, basestring):
        #                    object = URIRef(object)
        #                triples.append( (entity, Property.Properties['memberOf'].toPredicate(), object))

        triples += WikiResource(self.jsonDescription).toRDF()

        return triples
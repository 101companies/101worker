__author__ = 'avaranovich'

import os
import json

def handleType(t):
    onto = "onto:"
    if ':' in t:
        return t
    else:
        return (onto + t)

if __name__ == '__main__':

    relevant_path = os.path.join(os.path.dirname(__file__), 'models')
    included_extenstions = ['json']
    file_names = [fn for fn in os.listdir(relevant_path) if any([fn.endswith(ext) for ext in included_extenstions])]

    for file in file_names:
        print file
        s = \
            "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns> . \n\
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> . \n\
@prefix onto: <http://101companies.org/ontology#> . \n\
@prefix res: <http://101companies.org/resources#> . \n\
@prefix tech:<http://101companies.org/resources/Technology#> . \n\
@prefix lang:<http://101companies.org/resources/Language#> . \n\
@prefix concept:<http://101companies.org/resources/Concept#> . \n\
@prefix feature:<http://101companies.org/resources/Feature#> . \n\
@prefix contrib:<http://101companies.org/resources/Contribution#> . \n\
@prefix contributor:<http://101companies.org/resources/Contributor#> . \n\
@prefix voc:<http://101companies.org/resources/Vocabulary#> . \n\
@prefix theme:<http://101companies.org/resources/Theme#> . \n\
@prefix course:<http://101companies.org/resources/Course#> . \n\
@prefix script:<http://101companies.org/resources/Script#> . \n\
@prefix foaf: <http://xmlns.com/foaf/0.1/> . \n\n"


        with open(os.path.join(os.path.dirname(__file__), 'models', file)) as json_data:
            m = json.load(json_data)
            id = handleType(m['@id'])
            if m.has_key('@type'):
                t = m['@type']
                if type(t) is list:
                    s += id
                    for x in t:
                        s += " rdfs:subClassOf %s ; \n" % (handleType(x))
                else:
                    s += "%s rdfs:subClassOf %s ;" % (id, handleType(t))
                print(s)
            elif m.has_key('@instance'):
                t =  handleType(m['@instance'])
                s += "%s rdf:type %s ;" % (id, t)
                print(s)

            comment = ""
            if m.has_key('comment'):
                comment = m['comment']

            s += "\n    rdfs:comment \"%s\" . \n" % (comment)

            # :Entity rdfs:subclassOf owl:Class .

            if 'properties' in m:
                for prop in m['properties']:
                    print prop
                    comment = ""
                    if prop.has_key('comment'):
                        comment = prop['comment']
                    if not prop.has_key('overload'):
                        s += "\n\n %s rdfs:type rdfs:Property ; \n" \
                            " rdfs:comment \"%s\" ; \n" \
                            " rdfs:domain %s ; \n" \
                            " rdfs:range %s . \n" % (handleType(prop['property']), comment, id, prop['range'])

                    print s

                    # write output into ttl file
            with open(os.path.join(os.path.dirname(__file__), 'ttl', file.replace('.json', '.ttl')), 'w') as f:
                f.write(s)




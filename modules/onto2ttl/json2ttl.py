__author__ = 'avaranovich'

import os
import json

if __name__ == '__main__':

    relevant_path = os.path.join(os.path.dirname(__file__), 'models')
    included_extenstions = ['json']
    file_names = [fn for fn in os.listdir(relevant_path) if any([fn.endswith(ext) for ext in included_extenstions])]

    for file in file_names:
        print file
        with open(os.path.join(os.path.dirname(__file__), 'models', file)) as json_data:
            m = json.load(json_data)
            id = m['@id']
            if m.has_key('@type'):
                t = m['@type']
                s = ":%s rdfs:subclassOf %s ." % (id, t)
                print(s)
            elif m.has_key('@instance'):
                t = m['@instance']
                s = ":%s rdf:type %s ." % (id, t)
                print(s)

            # :Entity rdfs:subclassOf owl:Class .

            if 'properties' in m:
                for prop in m['properties']:
                    print prop
                    # TODO: comments are missing in the models
                    # " rdfs:label \"Name of the entity\" ; \n" \
                    # " rdfs:comment \"Comment\" ; \n" \
                    s += "\n\n %s rdfs:type rdfs:property ; \n" \
                         " rdfs:domain %s ; \n" \
                         " rdfs:range %s . \n" % (prop['property'], t, prop['range'])

                    print s

                # write output into ttl file
            with open(os.path.join(os.path.dirname(__file__), 'ttl', file.replace('.json','.ttl')), 'w') as f:
                f.write(s)




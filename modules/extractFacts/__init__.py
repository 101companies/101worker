#! /usr/bin/env python

import os
import sys
import json
sys.path.append('../../libraries/101meta')
sys.path.append('../../libraries')
import service_api
import const101
import tools101


# Per-file functionality
def derive(extractor, sFilename, tFilename):

   #print "Extract facts from " + sFilename + " with " + extractor + "."
   # sFilename = input
   # tFilename = output
   command = "{0} < \"{1}\" > \"{2}\"".format(os.path.join(const101.sRoot, extractor), sFilename, tFilename)

   (status, output) = tools101.run(command)

   return {
        'extractor': extractor,
        'command': command,
        'status': status,
        'output': output
    }

def main(data):
    data = service_api.expand_data(data)

    for f in data['data']:
        if os.path.exists(f + '.metadata.json'):
            metadata = json.load(open(f + '.metadata.json', 'r'))

            for match in metadata:
                for unit in match['metadata']:
                    if unit.has_key('extractor'):
                        derive(unit['extractor'], f, f + '.extractor.json')

if __name__ == '__main__':
    main({'data': ['/tmp/jaxbExtension/contributions/jaxbExtension'], 'type': 'folders'})

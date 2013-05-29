#! /usr/bin/env python

import os
import sys
import json
sys.path.append('../../libraries/101meta')
sys.path.append('../../libraries')
import service_api
import const101
import tools101


# Per-file functinonality
<<<<<<< HEAD
def derive(extractor, sFilename, tFilename):

   # Housekeeping for extractor
   #extractors.add(extractor)
   
   print "Extract facts from " + sFilename + " with " + extractor + "."
   # sFilename = input
   # tFilename = output
   command = "{0} < \"{1}\" > \"{2}\"".format(os.path.join(const101.sRoot, extractor), sFilename, tFilename)
=======
def derive(extractor, rFilename, sFilename, tFilename):

   # Housekeeping for extractor
   extractors.add(extractor)
   
   print "Extract facts from " + rFilename + " with " + extractor + "."
   command = "{0} < \"{1}\" > \"{2}\"".format(os.path.join(const101.sRoot, extractor),sFilename,tFilename)
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749
   (status, output) = tools101.run(command)

   # Result aggregation
   result = dict()
   result["extractor"] = extractor
   result["command"] = command
   result["status"] = status
   result["output"] = output

   return result

def main(data):
    data = service_api.expand_data(data)

    for f in data['data']:
        if os.path.exists(f + '.metadata.json'):
<<<<<<< HEAD
            metadata = json.load(open(f + '.metadata.json', 'r'))          
            
            for match in metadata:
                print match
                for unit in match['metadata']:
                    if unit.has_key('extractor'):
                        derive(unit['extractor'], f, f + '.extractor.json')
                    
if __name__ == '__main__':
    main({'data': ['/tmp/jaxbExtension/contributions/jaxbExtension'], 'type': 'folders'})

            
=======
            metadata = json.load(open(f + '.metadata.json', 'r'))
            # TODO: add stuff    
>>>>>>> 789459768f776d4d06b3c35544858ffc922ad749

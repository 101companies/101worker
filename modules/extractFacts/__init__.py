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
def derive(extractor, rFilename, sFilename, tFilename):

   # Housekeeping for extractor
   extractors.add(extractor)
   
   print "Extract facts from " + rFilename + " with " + extractor + "."
   command = "{0} < \"{1}\" > \"{2}\"".format(os.path.join(const101.sRoot, extractor),sFilename,tFilename)
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
            metadata = json.load(open(f + '.metadata.json', 'r'))
            # TODO: add stuff    

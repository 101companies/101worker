#!/usr/bin/env python
import json
import os
import subprocess
import meta101
from meta101.resource import File, Json

def initdump(deriver):
    for key in ["geshicodes", "extractors"]:
        if key in deriver.dump:
            deriver.dump[key] = set(deriver.dump[key])
        else:
            deriver.dump[key] = set()



def getextractor(deriver, resources, **kwargs):
    matches = resources[0]
    meta    = {}

    for m in matches:
        if "language" in m["metadata"]:
            extractorPath = os.path.join(os.environ["extractor101dir"],m["metadata"]["language"], "extractor")
            if os.path.isfile(extractorPath):
                 meta["extractor"] = extractorPath
        if "geshi" in m["metadata"]:
            meta["geshi"] = m["metadata"]["geshi"]

    if "geshi" in meta and "extractor" in meta:
        return meta

    raise ValueError()


def derive(deriver, value, resources, filename, **kwargs):
    extractor     = value["extractor"]
    geshicode     = value["geshi"]
    extractorpath = resources[1]

    deriver.dump["geshicodes"].add(geshicode)
    deriver.dump["extractors"].add(extractor)

    command = ["php", "helper.php", filename, geshicode, extractorpath]
    result  = json.loads(subprocess.check_output(command))
    return (result["metrics"], result["tokens"])


def preparedump(deriver):
    for key in ["geshicodes", "extractors"]:
        deriver.dump[key] = sorted(list(deriver.dump[key]))


changed = meta101.havechanged(__file__, "helper.php", "megalib_leftover.php")

meta101.derive(suffix    =[".fragments.metrics.json", ".fragments.tokens.json"],
               resources =[Json(".matches.json"), File(".extractor.json")],
               dump      =os.environ["fragmentMetrics101dump"],
               oninit    =initdump,
               getvalue  =getextractor,
               callback  =derive,
               ondump    =preparedump,
               entirerepo=changed)

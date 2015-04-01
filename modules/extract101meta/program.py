#!/usr/bin/env python
import os
import json
import subprocess
import meta101


def initdump(deriver):
    if "extractors" in deriver.dump:
        deriver.dump["extractors"] = set(deriver.dump["extractors"])
    else:
        deriver.dump["extractors"] = set()


def derive(deriver, language, filename, **kwargs):

    extractorPath = os.path.join(os.environ["extractor101dir"],language, "extractor")
    #extractorPath = os.environ["extractor101dir"] + "/" + language + "/extractor"
    if os.path.isfile(extractorPath):
        deriver.dump["extractors"].add(extractorPath)
        # extractors take their input via stdin, so we gotta open the file
        with open(filename) as f:
            return json.loads(subprocess.check_output([extractorPath], stdin=f))


def preparedump(deriver):
    deriver.dump["extractors"] = sorted(list(deriver.dump["extractors"]))

# FIXME also check extractors when they are moved into 101worker
changed = meta101.havechanged(__file__)

meta101.derive(suffix   =".extractor.json",
               dump     =os.environ["extractor101dump"],
               oninit   =initdump,
               getvalue ="language",
               callback =derive,
               ondump   =preparedump)

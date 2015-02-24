#!/usr/bin/env python
import os
import json
import subprocess
import meta101
import kludge101


def initdump(deriver):
    if "extractors" in deriver.dump:
        deriver.dump["extractors"] = set(deriver.dump["extractors"])
    else:
        deriver.dump["extractors"] = set()


def derive(deriver, extractor, filename, **kwargs):
    deriver.dump["extractors"].add(extractor)

    # FIXME move extractors into worker so this isn't necessary
    path = kludge101.checkpath(extractor)
    if not path:
        raise RuntimeError("foiled code injection: {}".format(extractor))

    # extractors take their input via stdin, so we gotta open the file
    with open(filename) as f:
        return json.loads(subprocess.check_output([path], stdin=f))


def preparedump(deriver):
    deriver.dump["extractors"] = sorted(list(deriver.dump["extractors"]))


# FIXME also check extractors when they are moved into 101worker
changed = meta101.havechanged(__file__)

meta101.derive(suffix    =".extractor.json",
               dump      =os.environ["extractor101dump"],
               oninit    =initdump,
               key       ="extractor",
               callback  =derive,
               ondump    =preparedump,
               entirerepo=changed)

#!/usr/bin/env python
import os
import subprocess
import meta101
import kludge101


def initdump(deriver):
    if "validators" in deriver.dump:
        deriver.dump["validators"] = set(deriver.dump["validators"])
    else:
        deriver.dump["validators"] = set()


def derive(deriver, validator, filename, **kwargs):
    deriver.dump["validators"].add(validator)

    path = os.path.join(os.environ["validator101dir"],validator, "validator")
    if not path:
        raise RuntimeError("foiled code injection: {}".format(validator))
    command = [path, filename]

    # subprocess has no safe getstatusoutput, so this'll have to do
    try:
        output, status = (subprocess.check_output(command), 0)
    except subprocess.CalledProcessError as e:
        output, status = (e.output, e.returncode)

    return {
        "validator" : validator,
        "command"   : command,
        "status"    : status,
        "output"    : output,
    }


def preparedump(deriver):
    deriver.dump["validators"] = sorted(list(deriver.dump["validators"]))


# FIXME also check validators when they are moved into 101worker
changed = meta101.havechanged(__file__)

meta101.derive(suffix    =".validator.json",
               dump      =os.environ["validator101dump"],
               oninit    =initdump,
               getvalue  ="validator",
               callback  =derive,
               ondump    =preparedump,
               entirerepo=changed)

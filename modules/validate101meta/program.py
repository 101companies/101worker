#!/usr/bin/env python
import os
import subprocess
import meta101


repo101dir = os.environ["repo101dir"]


def initdump(deriver):
    if "validators" in deriver.dump:
        deriver.dump["validators"] = set(deriver.dump["validators"])
    else:
        deriver.dump["validators"] = set()


def checkpath(validator):
    path = os.path.abspath(os.path.join(repo101dir, validator))
    # guard against paths with .. in them
    if not path.startswith(repo101dir):
        return None
    # blow up if there's a symlink somewhere
    dirs = path
    while len(dirs) > len(repo101dir):
        if os.path.islink(dirs):
            return None
        dirs = os.path.dirname(dirs)
    # XXX hopefully a safe path that only points to something in 101repo
    return path


def derive(validator, filename, **kwargs):
    validators.add(validator)

    # FIXME move validators into worker so this isn't necessary
    path = checkpath(validator)
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


meta101.derive(suffix  =".validator.json",
               dump    =os.environ["validator101dump"],
               oninit  =initdump,
               key     ="validator",
               callback=derive,
               ondump  =preparedump)

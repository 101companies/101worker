#!/usr/bin/env python
import os
import subprocess
import incremental101
import meta101


validators = set()
repo101dir = os.environ["repo101dir"]


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


# TODO load old dump


dump = meta101.derive(key     ="validator",
                      suffix  =".validator.json",
                      callback=derive)

dump["validators"] = list(validators)

incremental101.writejson(os.environ["validator101dump"], dump)

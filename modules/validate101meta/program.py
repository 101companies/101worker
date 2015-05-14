#!/usr/bin/env python
import os
import subprocess
import meta101


def initdump(deriver):
    if "validators" in deriver.dump:
        deriver.dump["validators"] = set(deriver.dump["validators"])
    else:
        deriver.dump["validators"] = set()


def derive(deriver, language, filename, **kwargs):

    path = os.path.join(os.environ["validator101dir"],language, "validator")

    if os.path.isfile(path):
        deriver.dump["validators"].add(path)
        command = [path, filename]

         # subprocess has no safe getstatusoutput, so this will have to do
        try:
            output, status = (subprocess.check_output(command), 0)
        except subprocess.CalledProcessError as e:
            output, status = (e.output, e.returncode)

        return {
            "validator" : path,
            "command"   : command,
            "status"    : status,
            "output"    : output,
         }


def preparedump(deriver):
    deriver.dump["validators"] = sorted(list(deriver.dump["validators"]))



vdir       = os.environ["validator101dir"]
validator = [os.path.join(vdir, d, "validator") for d in os.listdir(vdir)]
changed    = meta101.havechanged(__file__, "module.json", *validator )


meta101.derive(suffix    =".validator.json",
               dump      =os.environ["validator101dump"],
               oninit    =initdump,
               getvalue  ="language",
               callback  =derive,
               ondump    =preparedump,
               entirerepo=changed)

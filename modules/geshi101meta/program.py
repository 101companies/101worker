#!/usr/bin/env python
import os
import subprocess
import meta101


geshi = os.environ["gatheredGeshi101dir"] + "/run.php"


def initdump(deriver):
    if "geshicodes" in deriver.dump:
        deriver.dump["geshicodes"] = set(deriver.dump["geshicodes"])
    else:
        deriver.dump["geshicodes"] = set()


def derive(deriver, geshicode, filename, **kwargs):
    deriver.dump["geshicodes"].add(geshicode)
    command = ["php", geshi, filename, "php://stdout", geshicode]
    return subprocess.check_output(command)


def preparedump(deriver):
    deriver.dump["geshicodes"] = sorted(list(deriver.dump["geshicodes"]))


meta101.derive(suffix    =".geshi.html",
               dump      =os.environ["geshi101dump"],
               oninit    =initdump,
               getvalue  ="geshi",
               callback  =derive,
               ondump    =preparedump,
               entirerepo=meta101.havechanged(__file__))

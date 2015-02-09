#!/usr/bin/env python
import os
import subprocess
import incremental101
import meta101


geshi      = os.environ["gatheredGeshi101dir"] + "/run.php"
geshicodes = set()


def derive(geshicode, filename, **kwargs):
    geshicodes.add(geshicode)
    command = ["php", geshi, filename, "php://stdout", geshicode]
    return subprocess.check_output(command)


# TODO load old dump


dump = meta101.derive(key="geshi", suffix=".geshi.html", callback=derive)
dump["geshicodes"] = list(geshicodes)

incremental101.writejson(os.environ["geshi101dump"], dump)

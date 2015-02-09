#!/usr/bin/env python
import os
import incremental101
import meta101

geshi      = os.environ["gatheredGeshi101dir"] + "/run.php"
geshicodes = set()


def derive(geshicode, filename, **kwargs):
    geshicodes.add(geshicode)

    command        = ["php", geshi, filename, "php://stdout", geshicode]
    status, output = meta101.runcommand(*command)

    if status == 0:
        return output

    raise RuntimeError("{} exited with {}".format(" ".join(command), status))


dump = meta101.derive(key="geshi", suffix=".geshi.html", callback=derive)
dump["geshicodes"] = list(geshicodes)

incremental101.writejson(os.environ["geshi101dump"], dump)

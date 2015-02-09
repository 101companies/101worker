#!/usr/bin/env python
import os
import json
import subprocess
import incremental101
import meta101


geshicodes = set()


def getgeshi(deriver, matches):
    meta = {"relevance" : "system"}
    for m in matches:
        if "relevance" in m["metadata"]:
            meta["relevance"] = m["metadata"]["relevance"]
        if "geshi" in m["metadata"]:
            meta["geshi"] = m["metadata"]["geshi"]
    return meta


def derive(value, filename, **kwargs):
    relevance = value["relevance"]
    geshicode = value.get("geshi")

    if geshicode:
        geshicodes.add(geshicode)
        command = ["php", "helper.php", filename, geshicode, relevance]
        return json.loads(subprocess.check_output(command))
    else:
        return {
            "size"      : 0,
            "loc"       : 0,
            "sloc"      : 0,
            "relevance" : relevance,
            "tokens"    : [],
        }


# TODO load old dump


dump = meta101.derive(suffix  =".metrics.json",
                      callback=derive,
                      getvalue=getgeshi)

dump["geshicodes"] = list(geshicodes)

incremental101.writejson(os.environ["metrics101dump"], dump)

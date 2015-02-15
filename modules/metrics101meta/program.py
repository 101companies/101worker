#!/usr/bin/env python
import os
import json
import subprocess
import meta101


def initdump(deriver):
    if "geshicodes" in deriver.dump:
        deriver.dump["geshicodes"] = set(deriver.dump["geshicodes"])
    else:
        deriver.dump["geshicodes"] = set()


def getgeshi(deriver, matches, **kwargs):
    meta = {"relevance" : "system"}
    for m in matches:
        if "relevance" in m["metadata"]:
            meta["relevance"] = m["metadata"]["relevance"]
        if "geshi" in m["metadata"]:
            meta["geshi"] = m["metadata"]["geshi"]
    return meta


def derive(deriver, value, filename, **kwargs):
    relevance = value["relevance"]
    geshicode = value.get("geshi")

    if geshicode:
        deriver.dump["geshicodes"].add(geshicode)
        command = ["php", "helper.php", filename, geshicode, relevance]
        result  = json.loads(subprocess.check_output(command))
        return (result["metrics"], result["tokens"])

    return ({
                "size"      : 0,
                "loc"       : 0,
                "sloc"      : 0,
                "relevance" : relevance,
            }, [])


def preparedump(deriver):
    deriver.dump["geshicodes"] = sorted(list(deriver.dump["geshicodes"]))


meta101.derive(suffix  =[".metrics.json", ".tokens.json"],
               dump    =os.environ["metrics101dump"],
               oninit  =initdump,
               getvalue=getgeshi,
               callback=derive,
               ondump  =preparedump)

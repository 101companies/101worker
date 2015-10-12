#!/usr/bin/env python
from collections import OrderedDict
import json
import os
import meta101


defaults = OrderedDict([
    ("matches",       []),
    ("predicates",    []),
    ("fragments",     []),
    ("metrics",       {
        "size"      : 0,
        "loc"       : 0,
        "sloc"      : 0,
        "relevance" : "system",
    }),
    ("refinedTokens", []),
])


def readif(filename, default):
    try:
        with open(filename) as f:
            return json.load(f)
    except (IOError, ValueError):
        return default


def derive(deriver, value, resources, **kwargs):
    zipped = zip(resources, defaults.keys(), defaults.values())
    got    = {key : readif(path, default) for path, key, default in zipped}
    return {
        "units"         : got["matches"] + got["predicates"] + got["fragments"],
        "metrics"       : got["metrics"],
        "refinedTokens" : got["refinedTokens"],
    }


resrc = [meta101.resource.Pass(".{}.json".format(k)) for k in defaults.keys()]

meta101.derive(suffix    =".summary.json",
               dump      =os.environ["summary101dump"],
               getvalue  =lambda *args, **kwargs: True,
               callback  =derive,
               resources =resrc,
               entirerepo=meta101.havechanged(__file__))

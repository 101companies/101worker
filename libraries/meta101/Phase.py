import abc
import json
import os
import re
import incremental101
from   .util          import stripregex, tolist, diff, walk


class Phase(object):
    __metaclass__ = abc.ABCMeta


    def __init__(self, rules={}, matches=[], failures={}):
        self.rules    = rules
        self.matches  = {m["filename"]: m["units"] for m in matches}
        self.failures = failures


    @abc.abstractmethod
    def applicable(self, rule):
        pass # pragma: no cover


    def keys(self):
        return [
            "suffix",
            "filename",
            "basename",
            "dirname",
            "content",
        ]


    def dump(self):
        def tomatch(filename):
            return {
                "filename" : filename,
                "units"    : self.matches[filename],
            }

        return {
            "matches"  : [tomatch(key) for key in sorted(self.matches.keys())],
            "failures" : self.failures,
            "rules"    : self.rules,
        }


    def run(self, entirerepo=False):
        if entirerepo:
            walk(self.suffix, self.onfile)
            diff(self.suffix, D=self.ondelete)
        else:
            diff(self.suffix, A=self.onfile, M=self.onfile, D=self.ondelete)
        return self.dump()


    def cleandump(self, relative):
        if relative in self.matches:
            del self.matches[relative]
        if relative in self.failures:
            del self.failures[relative]


    def onfile(self, **kwargs):
        self.cleandump(kwargs["relative"])
        units = []

        for value in self.rules:
            rule   = value["rule"]
            result = self.match(rule, **kwargs)
            if result is not None and "metadata" in rule:
                for metadata in tolist(rule["metadata"]):
                    result["metadata"] = metadata
                    units.append(result.copy())

        # TODO fix this dominator code
        keys     = []
        for unit in units:
            metadata = unit["metadata"]
            if "dominator" in metadata:
                keys.append(metadata["dominator"])
        removals = []
        for key in keys:
            for unit in units:
                metadata = unit["metadata"]
                if key in metadata \
                and ("dominator" not in metadata
                     or metadata["dominator"] != key):
                    removals.append(unit)
        survivals = []
        for unit in units:
            if not unit in removals:
                survivals.append(unit)
        units = survivals

        if units:
            incremental101.writejson(kwargs["target"], units)
            self.matches[kwargs["relative"]] = units
        else:
            incremental101.deletefile(kwargs["target"])


    def ondelete(self, target, relative, **kwargs):
        incremental101.deletefile(target)
        self.cleandump(relative)


    def matchkey(self, key, rule, **kwargs):
        try:
            func = getattr(self, "check" + key, None)
            return func(rule[key], key=key, rule=rule, **kwargs)
        except Exception as e:
            self.failures[kwargs["relative"]] = {
                "error" : str(e),
                "key"   : key,
                "rule"  : rule,
            }
        return None


    def match(self, rule, **kwargs):
        if not self.applicable(rule):
            return None

        kwargs["result"] = {}
        for key in self.keys():
            if key in rule and not self.matchkey(key, rule, **kwargs):
                return None

        return kwargs["result"]


    def checksuffix(self, suffixes, basename, **kwargs):
        return any(basename.endswith(suffix) for suffix in tolist(suffixes))


    def checkcontent(self, pattern, filename, **kwargs):
        with open(filename) as f:
            return re.search(stripregex(pattern, pattern), f.read())


    def matchnames(self, values, path):
        def matchname(want):
            pattern = stripregex(want)
            return re.search(pattern, path) if pattern else path == want
        return any(matchname(v) for v in tolist(values))

    def checkfilename(self, values, relative, **kwargs):
        return self.matchnames(values, relative)

    def checkbasename(self, values, basename, **kwargs):
        return self.matchnames(values, basename)

    def checkdirname(self, values, dirname, **kwargs):
        return self.matchnames(values, dirname)

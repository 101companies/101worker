import abc
import json
import os
import re
import incremental101
from   .util          import stripregex, tolist, diff


class Phase(object):
    __metaclass__ = abc.ABCMeta


    def __init__(self, rules={}):
        # TODO make incrementality work for the big dump
        self.rules    = rules
        self.matches  = []
        self.failures = []


    @abc.abstractmethod
    def suffix(self):
        pass # pragma: no cover

    @abc.abstractmethod
    def applicable(self, rule):
        pass # pragma: no cover

    def dump(self):
        return {
            "matches"  : self.matches,
            "failures" : self.failures,
            "rules"    : self.rules,
        }


    def run(self):
        diff(self.suffix(), A=self.onfile, M=self.onfile, D=self.ondelete)
        return self.dump()


    def onfile(self, **kwargs):
        units = []

        for value in self.rules:
            # TODO short-circuit if the rule doesn't contain metadata?
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
            self.matches.append({
                "filename" : kwargs["relative"],
                "units"    : units,
            })
        else:
            incremental101.deletefile(kwargs["target"])


    def ondelete(self, target, **kwargs):
        incremental101.deletefile(target)


    def match(self, rule, **kwargs):
        if not self.applicable(rule):
            return None

        kwargs["result"] = {}
        for key in rule:
            func = getattr(self, "check" + key, None)
            if func and not func(rule[key], key=key, rule=rule, **kwargs):
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

    def checkfilename(self, values, filename, **kwargs):
        return self.matchnames(values, filename)

    def checkbasename(self, values, basename, **kwargs):
        return self.matchnames(values, basename)

    def checkdirname(self, values, dirname, **kwargs):
        return self.matchnames(values, dirname)

import abc
import json
import os
import re
import incremental101
from   util           import stripregex, tolist


class Phase(object):
    __metaclass__ = abc.ABCMeta


    def __init__(self, rules):
        self.rules   = rules
        self.matches = []


    @abc.abstractmethod
    def suffix(self):
        pass


    def run(self):
        repodir   = os.env[   "repo101dir"]
        targetdir = os.env["targets101dir"]
        switch    = {"A" : self.onfile, "M" : self.onfile, "D" : self.ondelete}

        for op, path in incremental101.gendiff():
            if path.startswith(repodir):
                target  = path.replace(repodir, targetdir, 1) + self.suffix()
                switch[op](target  =target,
                           filename=path,
                           dirname =os.path.dirname(path)[len(repodir):],
                           basename=os.path.basename(path))

        return self.matches


    def onfile(self, **kwargs):
        units = []

        for index, value in enumerate(self.rules):
            rule   = value["rule"]
            result = self.match(index, rule, **kwargs)
            if result and "metadata" in rule:
                for metadata in tolist(rule["metadata"]):
                    result["metadata"] = metadata
                    units.append(result.clone())

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
                and (not "dominator" in metadata
                     or not metadata["dominator"] == key):
                    removals.append(unit)
        survivals = []
        for unit in units:
            if not unit in removals:
                survivals.append(unit)
        units = survivals

        incremental101.writefile(target, json.dumps(units))
        if units:
            self.matches.append({
                "filename" : kwargs["filename"],
                "units"    : units,
            })


    def ondelete(self, target, **kwargs):
        incremental101.deletefile(target)


    def applicable(self, rule):
        return "fpredicate" not in rule

    def match(self, index, rule, **kwargs):
        if not self.applicable(rule):
            return None

        kwargs["result"] = {"id" : index}
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


    def matchname(self, want, path):
        pattern = stripregex(want)
        return re.search(pattern, path) if pattern else path == want

    def checkfilename(self, values, filename, **kwargs):
        return any(self.matchname(v, filename) for v in tolist(values))

    def checkbasename(self, values, basename, **kwargs):
        return self.checkfilename(values, basename)


    def matchdirname(self, want, path):
        pattern = stripregex(want)
        if pattern:
            match = re.search(pattern, path)
            return match and value[match.end() + 1] == "/"
        else:
            return path == want or path.startswith(want + "/")

    def checkdirname(self, values, dirname, **kwargs):
        return any(self.matchdirname(v, dirname) for v in tolist(values))

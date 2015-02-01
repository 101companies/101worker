import abc
import os
import incremental101


class Phase(object):
    __metaclass__ = abc.ABCMeta


    def __init__(rules):
        self.rules = rules


    @abc.abstractmethod
    def suffix(self):
        pass


    def run(self):
        repodir   = os.env[   "repo101dir"]
        targetdir = os.env["targets101dir"]
        switch    = {"A" : self.onfile, "M" : self.onfile, "D" : self.ondelete}

        for op, path in incremental101.gendiff():
            if path.startswith(repodir):
                target = path.replace(repodir, targetdir, 1) + self.suffix()
                switch[op](**{
                    "target"   : target,
                    "filename" : path,
                    "dirname"  : os.path.dirname (path),
                    "basename" : os.path.basename(path),
                })


    def onfile(self, **kwargs):
        units = []

        for index, value in enumerate(self.rules):
            rule   = value["rule"]
            result = self.match(index, rule, **kwargs)
            if result and "metadata" in rule:
                for metadata in tolist(rule["metadata"]):
                    result["metadata"] = metadata
                    units.append(result.clone())


    def ondelete(self, target, **kwargs):
        incremental101.deletefile(target)


    def applicable(self, rule):
        return "fpredicate" not in rule

    def match(self, index, rule, **kwargs):
        if not self.applicable(rule):
            return None

        result = {"id" : index}
        for key in rule:
            func = getattr(self, "check" + key, None)
            if func and not func(rule[key], key=key, rule=rule, **kwargs):
                return None

        return result


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


    def checksuffix(self, suffixes, basename, **kwargs):
        return any(basename.endswith(suffix) for suffix in tolist(suffixes))


    def checkcontent(self, pattern, source, **kwargs):
        with open(source) as f:
            return re.search(stripregex(pattern, pattern), f.read())

"""
Match 101rules base class. See the main module's matchall function.
"""
import abc
import re
import incremental101
from   .util          import stripregex, tolist, diff, walk


class Phase(object):
    """
    Base for matching 101rules. The various phases extend this class. As of
    the time of writing, those classes are Matches, Predicates and Fragments.

    Note that method and attribute names starting with ``check'' are reserved
    for rule handlers.

    Any subclass must also have a suffix attribute representing its derived
    resource suffix.
    """
    __metaclass__ = abc.ABCMeta


    def __init__(self, rules={}, matches=[], failures={}):
        """
        Construct a new Phase with the given rules dump, matches dump and
        failures.
        """
        self.rules    = rules
        self.matches  = {m["filename"]: m["units"] for m in matches}
        self.failures = failures


    @abc.abstractmethod
    def applicable(self, rule):
        """
        This function must be overridden in subclasses. It must return a true
        value when the given rule is applicable to the current phase and a
        false value otherwise.
        """
        pass # pragma: no cover


    def keys(self):
        """
        Returns a list of rule keys to be checked by this phase. Subclasses
        may override this and add additional keys.
        """
        return [
            "suffix",
            "filename",
            "basename",
            "dirname",
            "content",
        ]


    def dump(self):
        """
        Creates a dump from this phase's attributes. May be overridden by
        subclasses if they have something to add to it other than matches,
            failures and the rules dump.
        """
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
        """
        Executes the matching of 101rules. If entirerepo is a true value, all
        files of 101repo are re-derived. Otherwise, only new or modified files
        are handled. Deleted files, however, are always deleted.
        """
        if entirerepo:
            walk(self.suffix, self.onfile)
            # diff(self.suffix, [], D=self.ondelete)
        else:
            diff(self.suffix, [], A=self.onfile, M=self.onfile, D=self.ondelete)
        return self.dump()


    def cleandump(self, relative):
        """
        Removes the given relative file path from the phase's matches and
        failures.
        """
        if relative in self.matches:
            del self.matches[relative]
        if relative in self.failures:
            del self.failures[relative]


    def onfile(self, **kwargs):
        """
        Derives metadata from for a file from 101repo. Called when a file was
        added or changed, or if the entire repo is walked to re-derive all
        files.
        """
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
        """
        Removes all traces of a deleted primary resource created by this phase.
        """
        incremental101.deletefile(target)
        self.cleandump(relative)


    def matchkey(self, key, rule, **kwargs):
        """
        Runs a check method for the given rule and key. If a method called
        `"check" + rule` exists, it is called wth the given key, rule and
        **kwargs and its value is returned. If the value is true, matching
        continues, otherwise it counts as no match.

        Any Exception raised is caught and added to this phase's failures. If
        that happens or the method with the correct name doesn't exist, None
        is returned.
        """
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
        """
        Attempts to match the given rule with this phase. If any of the check
        methods return a false value, the match is unsuccessful. See matchkey.

        Returns match result dict if the match was successful and None
        otherwise.
        """
        if not self.applicable(rule):
            return None

        kwargs["result"] = {}
        for key in self.keys():
            if key in rule and not self.matchkey(key, rule, **kwargs):
                return None

        return kwargs["result"]


    def checksuffix(self, suffixes, basename, **kwargs):
        """
        Checks if the primary resource ends with the given suffix or list of
        suffixes.
        """
        return any(basename.endswith(suffix) for suffix in tolist(suffixes))


    def checkcontent(self, pattern, filename, **kwargs):
        """
        Checks if the content of the primary resource matches the given regex
        pattern.
        """
        with open(filename) as f:
            return re.search(stripregex(pattern, pattern), f.read())


    def matchnames(self, values, path):
        """
        Returns if the given path matches the given value or list of values. If
        a value is surrounded by #, it is interpreted as a regex pattern,
        otherwise it's an exact match.
        """
        def matchname(want):
            pattern = stripregex(want)
            return re.search(pattern, path) if pattern else path == want
        return any(matchname(v) for v in tolist(values))


    def checkfilename(self, values, relative, **kwargs):
        """
        Checks if the primary resource's relative path matches the given value
        or values. See matchnames.
        """
        return self.matchnames(values, relative)


    def checkbasename(self, values, basename, **kwargs):
        """
        Checks if the primary resource's basename matches the given value
        or values. See matchnames.
        """
        return self.matchnames(values, basename)


    def checkdirname(self, values, dirname, **kwargs):
        """
        Checks if the primary resource's dirname matches the given value
        or values. See matchnames.
        """
        return self.matchnames(values, dirname)

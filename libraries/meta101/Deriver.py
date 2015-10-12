"""
Deriving 101meta resources. See the main module's derive function.
"""
import json
import sys
import incremental101
from .        import resource
from .Matches import Matches
from .util    import diff, tolist, sourcetotarget, valuebykey, walk


class Deriver(object):
    """
    Class for deriving 101meta resources.
    """


    def __init__(self, suffix, dump, callback, getvalue, oninit=None,
                 ondump=None, resources=None):
        """
        Construct a deriver object. See the main module's derive function for
        documentation about these parameters.
        """
        self.suffix      = suffix
        self.dumppath    = dump
        self.dump        = self.loaddump(dump)
        self.suffixcount = 1 if type(suffix) is str else len(suffix)
        self.callback    = callback
        self.ondump      = ondump
        self.resources   = resources or resource.Json(Matches.suffix)
        if callable(getvalue):
            self.getvalue = getvalue
        else:
            self.getvalue = lambda deriver, matches, **kwargs: \
                                valuebykey(getvalue, matches)
        if oninit:
            oninit(self)


    def run(self, entirerepo=False):
        """
        Executes this deriver. If entirerepo is a true value, all files of
        101repo are re-derived. Otherwise, only new or modified files are
        handled. Deleted files, however, are always deleted.
        """
        if entirerepo:
            walk(self.suffix, self.onfile)
            diff(self.suffix, tolist(self.resources), D=self.ondelete)
        else:
            diff(self.suffix, tolist(self.resources), A=self.onfile,
                 M=self.onfile, D=self.ondelete)

        if self.ondump:
            self.ondump(self)

        incremental101.writejson(self.dumppath, self.dump)


    @staticmethod
    def loaddump(path):
        """
        Attempts to load and return the dump at the given path. If an IOError
        occurs, returns the default dump.
        """
        try:
            with open(path) as f:
                return json.load(f)
        except IOError:
            return {"problems" : {}}


    def rmdump(self, key):
        """
        Removes the given key from this deriver's dump's problems, if it
        exists.
        """
        if key in self.dump["problems"]:
            del self.dump["problems"][key]


    def loadresources(self, path):
        """
        Loads this deriver's resources for the given path.
        """
        load = [r.load(sourcetotarget(path)) for r in tolist(self.resources)]
        return load[0] if isinstance(self.resources, resource.Pass) else load


    def onfile(self, **kwargs):
        """
        Handles modification or addition of a file to be derived. See the
        main module's documentation about how this goes about.
        """
        self.rmdump(kwargs["relative"])

        try:
            resources = self.loadresources(kwargs["filename"])
            value     = self.getvalue(self, resources, **kwargs)
        except Exception:
            for t in tolist(kwargs["target"]):
                incremental101.deletefile(t)
            return

        try:
            result = self.callback(self, value, resources=resources, **kwargs)
        except Exception as e:
            self.dump["problems"][kwargs["relative"]] = str(e)
            for t in tolist(kwargs["target"]):
                incremental101.deletefile(t)
            return

        if type(result) is not tuple:
            result = (result,)

        if len(result) != self.suffixcount:
            sys.exit("Expected {}-tuple for suffix(es) {}, but got this "
                     "{}-tuple instead: {}".format(self.suffixcount,
                     self.suffix, len(result), result))

        for r, t in zip(result, tolist(kwargs["target"])):
            if r is None:
                incremental101.deletefile(t)
            elif type(r) in [dict, list]:
                incremental101.writejson(t, r)
            else:
                incremental101.writefile(t, r)


    def ondelete(self, target, relative, **kwargs):
        """
        Handles the deletion of a resource. Removes its entry in the dump and
        any derived files, if they exist.
        """
        self.rmdump(relative)
        for t in tolist(target):
            incremental101.deletefile(t)

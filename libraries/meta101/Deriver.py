import json
import os
import sys
import incremental101
from   .Matches       import Matches
from   .util          import diff, tolist, sourcetotarget, valuebykey, walk


class Deriver(object):


    def __init__(self, suffix, dump, callback, oninit=None, ondump=None,
                 getvalue=valuebykey, key=None, resources=None):
        self.key         = key
        self.suffix      = suffix
        self.dumppath    = dump
        self.dump        = self.loaddump(dump)
        self.suffixcount = 1 if type(suffix) is str else len(suffix)
        self.callback    = callback
        self.getvalue    = getvalue
        self.ondump      = ondump
        self.resources   = resources or "json:" + Matches.suffix
        if oninit:
            oninit(self)


    def run(self, entirerepo=False):
        if entirerepo:
            walk(self.suffix, self.onfile)
            diff(self.suffix, D=self.ondelete)
        else:
            diff(self.suffix, A=self.onfile, M=self.onfile, D=self.ondelete)

        if self.ondump:
            self.ondump(self)

        incremental101.writejson(self.dumppath, self.dump)


    def loaddump(self, path):
        try:
            with open(path) as f:
                return json.load(f)
        except IOError:
            return {"problems" : {}}


    def rmdump(self, key):
        if key in self.dump["problems"]:
            del self.dump["problems"][key]


    def loadresources(self, filename):
        target = sourcetotarget(filename)
        loaded = []

        for resource in tolist(self.resources):
            what, suffix = resource.split(":", 2)
            path         = target + suffix
            if not os.path.exists(path):
                raise ValueError()

            if   what == "path":
                loaded.append(path)
            elif what == "json":
                with open(path) as f:
                    loaded.append(json.load(f))
            else:
                sys.exit("invalid resource {} in {}".format(what, resource))

        return loaded[0] if type(self.resources) is str else loaded


    def onfile(self, **kwargs):
        self.rmdump(kwargs["relative"])

        try:
            resources = self.loadresources(kwargs["filename"])
            value     = self.getvalue(self, resources, **kwargs)
        except Exception:
            return

        try:
            result = self.callback(self, value, resources=resources, **kwargs)
        except Exception as e:
            self.dump["problems"][kwargs["relative"]] = str(e)
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
        self.rmdump(relative)
        for t in tolist(target):
            incremental101.deletefile(t)

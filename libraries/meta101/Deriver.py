import json
import os
import incremental101
from   .util          import diff, tolist, sourcetotarget, valuebykey


class Deriver(object):


    def __init__(self, suffix, dump, callback, key=None, oninit=None,
                 getvalue=valuebykey, ondump=None):
        self.key         = key
        self.suffix      = suffix
        self.dumppath    = dump
        self.dump        = self.loaddump(dump)
        self.suffixcount = 1 if type(suffix) is str else len(suffix)
        self.callback    = callback
        self.getvalue    = getvalue
        self.ondump      = ondump
        if oninit:
            oninit(self)


    def derive(self):
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


    def onfile(self, **kwargs):
        self.rmdump(kwargs["relative"])

        try:
            matchesfile = sourcetotarget(kwargs["filename"]) + ".matches.json"
            with open(matchesfile) as f:
                matches = json.load(f)
            value = self.getvalue(self, matches, **kwargs)
        except Exception:
            return

        try:
            result = self.callback(self, value, **kwargs)
        except Exception as e:
            self.dump["problems"][kwargs["relative"]] = str(e)
            return

        if type(result) is not tuple:
            result = (result,)

        if len(result) != self.suffixcount:
            raise TypeError("Expected {}-tuple for suffix(es) {}, but got this "
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

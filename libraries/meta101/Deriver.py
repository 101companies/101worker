import json
import os
import incremental101
from   .util          import diff, tolist, sourcetotarget, valuebykey


class Deriver(object):


    def __init__(self,
                 suffix,
                 callback,
                 key     =None,
                 getvalue=valuebykey,
                 dump    ={"problems" : {}}):
        self.key      = key
        self.suffix   = suffix
        self.callback = callback
        self.dump     = dump
        self.getvalue = getvalue


    def derive(self):
        diff(self.suffix, A=self.onfile, M=self.onfile, D=self.ondelete)
        return self.dump


    def rmdump(self, target):
        if target in self.dump["problems"]:
            del self.dump["problems"][target]


    def onfile(self, target, **kwargs):
        self.rmdump(str(target))

        try:
            matchesfile = sourcetotarget(kwargs["filename"]) + ".matches.json"
            with open(matchesfile) as f:
                matches = json.load(f)
            value = self.getvalue(self, matches)
        except Exception:
            return

        try:
            result = self.callback(value, target=target, **kwargs)

            if type(result) is not tuple:
                result = (result,)

            for r, t in zip(result, tolist(target)):
                if r is None:
                    incremental101.deletefile(t)
                elif type(r) in [dict, list]:
                    incremental101.writejson(t, r)
                else:
                    incremental101.writefile(t, r)

        except Exception as e:
            self.dump["problems"][str(target)] = str(e)


    def ondelete(self, target, **kwargs):
        self.rmdump(str(target))
        for t in tolist(target):
            incremental101.deletefile(t)

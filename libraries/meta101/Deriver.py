import os
import incremental101
from   .util          import diff


class Deriver(object):


    def __init__(self, key, suffix, callback, dump={"problems" : {}}):
        self.key      = key
        self.suffix   = suffix
        self.callback = callback


    def derive(self):
        diff(self.suffix, A=self.onfile, M=self.onfile, D=self.ondelete)
        return self.dump


    def rmdump(self, key):
        if key in dump["problems"]:
            del dump["problems"][key]


    def onfile(self, target, **kwargs):
        self.rmdump(target)

        if not MATCHES:
            return

        try:
            result = self.callback(VALUE, target=target, **kwargs)
            if result is None:
                incremental101.deletefile(target)
            elif type(result) in [dict, list]:
                incremental101.writejson(target, result)
            else:
                incremental101.writefile(target, result)

        except Exception as e:
            self.dump["problems"][target] = str(e)


    def ondelete(self, target, **kwargs):
        self.rmdump(filename)
        incremental101.deletefile(target)

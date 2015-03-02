import json
import os
from .util import sourcetotarget


class Pass(object):

    def __init__(self, suffix):
        self.suffix = suffix

    def load(self, filename):
        return filename + self.suffix


class File(Pass):

    def load(self, filename):
        target = super(File, self).load(filename)
        if os.path.exists(target):
            return target
        raise ValueError("File doesn't exist: {}".format(target))


class Json(File):

    def load(self, filename):
        with open(super(Json, self).load(filename)) as f:
            return json.load(f)

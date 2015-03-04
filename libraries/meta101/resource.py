"""
Resources used by the Deriver. They have various levels of sophistication.

The interface for resources is just the load method, which takes a filename
parameter. It may either return the actual resource or raise a ValueError if
the resource doesn't exist or something is wrong with it.
"""
import json
import os


class Pass(object):
    """
    Basic resource, just a pass-through.
    """
    def __init__(self, suffix):
        """
        Create a resource with the given suffix. Your suffix must include the
        initial dot, so it's ".suffix.json", not "suffix.json".
        """
        self.suffix = suffix

    def load(self, filename):
        """
        Returns the filename with the suffix attached to it - i.e. the path of
        the resource.
        """
        return filename + self.suffix


class File(Pass):
    """
    Resource for a file that must exist, rather than just passing through
    anything given to it.
    """

    def load(self, filename):
        """
        Returns the filename with the suffix attached to it if the resource
        exists. Otherwise raises a ValueError complaining about it.
        """
        target = super(File, self).load(filename)
        if os.path.exists(target):
            return target
        raise ValueError("File doesn't exist: {}".format(target))


class Json(File):
    """
    Resource for a JSON file that is to be decoded.
    """

    def load(self, filename):
        """
        Returns the decoded JSON from the resource. Raises a ValueError if the
        file doesn't exist or if it can't be decoded.
        """
        with open(super(Json, self).load(filename)) as f:
            return json.load(f)

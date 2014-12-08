__author__ = 'martin'

import os
import commands
import sys
sys.path.append('../../libraries/101meta')
import const101


class ChangeObject():
    @classmethod
    def parse(cls, output, path=None):
        results = []
        lines = output.splitlines()
        for line in lines:
            op, file = line.split("\t")
            if path:
                os.path.join(path, file)
            results.append(ChangeObject(op, file))

        return results

    def __init__(self, operation, filepath):
        """
        @type operation: str
        @type filepath: str
        """

        def sanitize(path):
            s = path.replace(const101.sRoot, "")
            if s[0] == "/": s = s[1:]
            return s

        self.__operation = operation
        self.__filepath = sanitize(filepath)

    @property
    def operation(self):
        return self.__operation

    @property
    def path(self):
        """
        @rtype : str
        """
        return self.__filepath

    @path.setter
    def path(self, value):
        self.__filepath = value

    def __str__(self):
        return "({}, {})".format(self.operation, self.path)

    def __repr__(self):
        return self.__str__()


class Repo():
    def __init__(self, url, path):
        """
        @type path: str
        @type url: str
        """
        self.__path = os.path.abspath(path)
        self.__url = url

    @property
    def exists(self):
        return os.path.exists(os.path.join(self.__path, ".git"))

    def cloneOrPull(self):
        if self.exists:
            return self.pull()
        else:
            return self.clone()

    def clone(self):
        cmd = "git clone {} {}".format(self.__url, self.__path)
        status, output = commands.getstatusoutput(cmd)
        if not status == 0: raise Exception(output)

        added = []
        for root, dirs, files in os.walk(self.__path):
            if not '.git' in root:
                added += [ChangeObject("A", os.path.join(root, path)) for path in files]
        return added

    def pull(self):
        cmd = "git --git-dir={} --work-tree={} pull"\
              .format(os.path.join(self.__path, ".git"), self.__path)
        status, output = commands.getstatusoutput(cmd)
        if not status == 0: raise Exception(output)

        if "Already up-to-date." in output:
            return []

        cmd = "git --git-dir={} diff --name-status HEAD^ HEAD".format(os.path.join(self.__path, ".git"))
        return ChangeObject.parse(commands.getoutput(cmd), self.__path)
